import click
import tempfile
import json
from typing import Dict, List, Optional, Any
import anyio
from mcp.server.lowlevel import Server
import mcp.types as types
from openapi_parser import OpenAPIToolsManager
from mcp.server.fastmcp.prompts import Prompt, PromptManager
from custom_prompts import create_agent_prompt

class MCPOpenAPIServer:
    """MCP Server that provides OpenAPI tools and prompts."""
    
    def __init__(self, spec_path: str):
        """Initialize the server with an OpenAPI specification."""
        with open(spec_path, 'r') as file:
            spec = json.load(file)
        
        # Create a temporary file to save the spec as a string, note: to be removed later
        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.json') as tmp_file:
            # Write the loaded spec as a JSON string to the temporary file
            json.dump(spec, tmp_file)
            temp_spec_path = tmp_file.name
        

        

        self.api_tools = OpenAPIToolsManager(temp_spec_path)
        self.app = Server(name="mcp-openapi-tools-and-prompts")
        self.prompt_manager = PromptManager(warn_on_duplicate_prompts=True)
        
        # Register prompts
        self._register_prompts()
        
        # Set up handlers
        self._setup_handlers()
    
    def _register_prompts(self):
        """Register all prompts with the prompt manager."""
        # Create agent prompt
        create_agent = Prompt.from_function(
            create_agent_prompt,
            name="create_agent",
            description="Create an agent with a specific model, instructions, and tool groups"
        )
        self.prompt_manager.add_prompt(create_agent)
    
    def _setup_handlers(self):
        """Set up handlers for the MCP server."""
        @self.app.list_tools()
        async def list_tools() -> List[types.Tool]:
            return self._get_tools()
            
        @self.app.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent | types.ImageContent | types.EmbeddedResource]:
            return await self._execute_tool(name, arguments)
            
        @self.app.list_prompts()
        async def list_prompts() -> List[types.Prompt]:
            return self._get_prompts()
            
        @self.app.get_prompt()
        async def get_prompt(name: str, arguments: Optional[Dict[str, str]] = None) -> types.GetPromptResult:
            return await self._get_prompt_result(name, arguments)
    
    async def _execute_tool(self, name: str, arguments: Dict[str, Any]) -> List[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        """Execute a tool by name with the given arguments."""
        try:
            # Initialize client if needed
            if self.api_tools.client is None:
                await self.api_tools.initialize_client()
                
            result = await self.api_tools.execute_api_call(name, arguments)
            
            content_type = result.get('content_type', '')
            data = result.get('data', '')
            
            if 'application/json' in content_type:
                if isinstance(data, dict) or isinstance(data, list):
                    return [types.TextContent(type="text", text=json.dumps(data, indent=2))]
                else:
                    return [types.TextContent(type="text", text=str(data))]
            elif 'image/' in content_type and isinstance(data, bytes):
                return [types.ImageContent(type="image", data=data)]
            else:
                return [types.TextContent(type="text", text=str(data))]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error executing tool: {str(e)}")]
    
    def _get_tools(self) -> List[types.Tool]:
        """Get a list of all tools from the OpenAPI specification."""
        tools = []
        
        for endpoint in self.api_tools.get_endpoints():
            tools.append(types.Tool(
                name=endpoint['operation_id'],
                description=endpoint.get('summary', '') or endpoint.get('description', '') or f"Call {endpoint['method'].upper()} {endpoint['path']}",
                inputSchema=self.api_tools.generate_input_schema(endpoint)
            ))
        
        return tools
    
    def _get_prompts(self) -> List[types.Prompt]:
        """Get a list of all available prompts."""
        return [
            types.Prompt(
                name=prompt.name,
                description=prompt.description,
                arguments=[
                    types.PromptArgument(
                        name=arg.name,
                        description=arg.description,
                        required=arg.required,
                    )
                    for arg in (prompt.arguments or [])
                ],
            )
            for prompt in self.prompt_manager.list_prompts()
        ]
    
    async def _get_prompt_result(
        self, name: str, arguments: Optional[Dict[str, str]] = None
    ) -> types.GetPromptResult:
        """Get the prompt result for a specific prompt."""
        if arguments is None:
            arguments = {}
            
        try:
            messages = await self.prompt_manager.render_prompt(name, arguments)
            
            # Convert messages to the format expected by MCP
            mcp_messages = []
            for msg in messages:
                mcp_messages.append(
                    types.PromptMessage(
                        role=msg["role"],
                        content=types.TextContent(
                            type="text", text=msg["content"]
                        ),
                    )
                )
            
            return types.GetPromptResult(
                messages=mcp_messages,
                description=f"Prompt for {name}",
            )
        except Exception as e:
            raise ValueError(f"Error rendering prompt {name}: {str(e)}")
    
    async def run(self, transport: str, port: int):
        """Run the MCP server with the specified transport."""
        # Initialize the HTTP client
        await self.api_tools.initialize_client()
        
        try:
            if transport == "sse":
                await self._run_sse(port)
            else:
                await self._run_stdio()
        finally:
            # Clean up the HTTP client
            await self.api_tools.close_client()
    
    async def _run_sse(self, port: int):
        """Run the server with SSE transport."""
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        from starlette.routing import Mount, Route
        import uvicorn
        
        sse = SseServerTransport("/messages/")
        
        async def handle_sse(request):
            async with sse.connect_sse(
                request.scope, request.receive, request._send
            ) as streams:
                await self.app.run(
                    streams[0], streams[1], self.app.create_initialization_options()
                )
        
        starlette_app = Starlette(
            debug=True,
            routes=[
                Route("/sse", endpoint=handle_sse),
                Mount("/messages/", app=sse.handle_post_message),
            ],
        )
        
        config = uvicorn.Config(starlette_app, host="0.0.0.0", port=port)
        server = uvicorn.Server(config)
        await server.serve()
    
    async def _run_stdio(self):
        """Run the server with stdio transport."""
        from mcp.server.stdio import stdio_server
        
        async with stdio_server() as streams:
            await self.app.run(
                streams[0], streams[1], self.app.create_initialization_options()
            )

@click.command()
@click.argument('spec_path')
@click.option("--port", default=8000, help="Port to listen on for SSE")
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse"]),
    default="stdio",
    help="Transport type",
)
def main(spec_path: str, port: int, transport: str) -> int:
    """Create MCP server with tools from an OpenAPI specification and custom prompts."""
    server = MCPOpenAPIServer(spec_path)
    
    async def run_server():
        await server.run(transport, port)
    
    anyio.run(run_server)
    return 0

if __name__ == "__main__":
    main()