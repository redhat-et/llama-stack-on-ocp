import pytest
import os
import json
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
from dotenv import load_dotenv
from llama_stack_client import LlamaStackClient
from llama_stack_client.lib.agents.agent import Agent
from llama_stack_client.lib.agents.event_logger import EventLogger


# Load environment variables for tests
load_dotenv()


# Configure logging
@pytest.fixture(scope="session")
def logger():
    """Set up logging for tests."""
    logger = logging.getLogger("mcp_test")
    if logger.hasHandlers():
        logger.handlers.clear()
    
    logger.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    file_handler = logging.FileHandler(log_dir / "mcp_test.log")
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    return logger


# Fixtures for test resources
@pytest.fixture(scope="session")
def llama_client():
    """Create and return a LlamaStackClient."""
    base_url = os.getenv('REMOTE_BASE_URL')
    if not base_url:
        pytest.skip("REMOTE_BASE_URL environment variable not set")
    
    return LlamaStackClient(base_url=base_url)


@pytest.fixture(scope="session")
def test_configs():
    """Return test configurations for different MCP servers."""
    return {
        "ansible": {
            "file_path": './queries/anisble_queries.json',
            "mcp_url": os.getenv('ANSIBLE_MCP_SERVER_URL'),
            "toolgroup_id": "mcp::ansible"
        },
        "github": {
            "file_path": './queries/github_queries.json',
            "mcp_url": os.getenv('GITHUB_MCP_SERVER_URL'),
            "toolgroup_id": "mcp::github"
        },
        "openshift": {
            "file_path": './queries/ocp_queries.json',
            "mcp_url": os.getenv('OCP_MCP_SERVER_URL'),
            "toolgroup_id": "mcp::openshift"
        },
        "custom": {
            "file_path": './queries/custom_queries.json',
            "mcp_url": os.getenv('CUSTOM_MCP_SERVER_URL'),
            "toolgroup_id": "mcp::custom_tool"
        }
    }


def load_queries(file_path: str) -> List[str]:
    """Load query strings from a JSON file."""
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        if not isinstance(data, dict) or 'queries' not in data:
            pytest.fail(f"Invalid JSON format in {file_path}")
        
        return [query['query'] for query in data['queries']]
    except FileNotFoundError:
        pytest.fail(f"Query file not found: {file_path}")
    except json.JSONDecodeError:
        pytest.fail(f"Invalid JSON in file: {file_path}")


def register_toolgroup_if_needed(
    client: LlamaStackClient, 
    toolgroup_id: str, 
    mcp_url: str, 
    logger: logging.Logger
) -> None:
    """Register a toolgroup if it doesn't exist."""
    try:
        registered_tools = client.tools.list()
        registered_toolgroups = set(t.toolgroup_id for t in registered_tools)
        
        logger.info(f"Available toolgroups: {registered_toolgroups}")
        
        if toolgroup_id not in registered_toolgroups:
            logger.info(f"Registering toolgroup: {toolgroup_id}")
            client.toolgroups.register(
                toolgroup_id=toolgroup_id,
                provider_id="model-context-protocol",
                mcp_endpoint={"uri": mcp_url},
            )
            logger.info(f"Successfully registered toolgroup: {toolgroup_id}")
        else:
            logger.info(f"Toolgroup {toolgroup_id} is already registered")
    except Exception as e:
        pytest.fail(f"Failed to register toolgroup {toolgroup_id}: {e}")


def execute_query(
    client: LlamaStackClient,
    prompt: str,
    model: str,
    toolgroup_id: str,
    logger: logging.Logger,
    instructions: Optional[str] = None,
    max_tokens: int = 4096
) -> Dict[str, Any]:
    """Execute a single query."""
    if instructions is None:
        instructions = """You are a helpful assistant. You have access to a number of tools.
            Whenever a tool is called, be sure return the Response in a friendly and helpful tone.
            When you are asked to search the web you must use a tool. Keep answers concise.
            """
    
    # Create agent with tools
    agent = Agent(
        client,
        model=model,
        instructions=instructions,
        tools=[toolgroup_id],
        tool_config={"tool_choice": "auto"},
        sampling_params={"max_tokens": max_tokens}
    )
    
    # Create session
    import time
    session_id = agent.create_session(session_name=f"Test_{toolgroup_id}_{int(time.time())}")
    
    # Execute query
    turn_response = agent.create_turn(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        session_id=session_id
    )
    
    return turn_response


# Test class for each MCP server type
class TestMCPServer:
    """Test class for testing MCP servers."""
    
    @pytest.fixture(autouse=True)
    def setup(self, logger, llama_client, test_configs, request):
        """Set up test environment."""
        self.logger = logger
        self.client = llama_client
        self.test_configs = test_configs
        self.results_dir = Path("results")
        self.results_dir.mkdir(exist_ok=True)
    
    @pytest.mark.parametrize("server_type", ["ansible", "github", "openshift", "custom"])
    def test_server_connection(self, server_type):
        """Test that we can connect to the MCP server."""
        config = self.test_configs[server_type]
        
        # Skip if MCP URL is not set
        if not config["mcp_url"]:
            pytest.skip(f"MCP URL for {server_type} not set in environment variables")
        
        # Try to register the toolgroup
        register_toolgroup_if_needed(
            self.client, 
            config["toolgroup_id"], 
            config["mcp_url"], 
            self.logger
        )
        
        # If we got here, the connection works
        assert True
    
    @pytest.mark.parametrize("server_type", ["github", "openshift", "custom"])
    @pytest.mark.parametrize("model", ["meta-llama/Llama-3.2-3B-Instruct", "ibm-granite/granite-3.2-8b-instruct"])
    def test_queries(self, server_type, model):
        """Test queries for a specific MCP server with different models."""
        config = self.test_configs[server_type]
        
        # Skip if MCP URL is not set
        if not config["mcp_url"]:
            pytest.skip(f"MCP URL for {server_type} not set in environment variables")
        
        # Load queries
        queries = load_queries(config["file_path"])
        if not queries:
            pytest.skip(f"No queries found in {config['file_path']}")
        
        # Test each query
        self.logger.info(f"Testing {len(queries)} queries for {server_type} with model {model}")
        
        successful_queries = 0
        
        for i, prompt in enumerate(queries, 1):
            self.logger.info(f"Query {i}/{len(queries)}: {prompt[:50]}...")
            
            try:
                response = execute_query(
                    self.client,
                    prompt,
                    model,
                    config["toolgroup_id"],
                    self.logger
                )
                
                # Log the response
                self.logger.info(f"Query {i} succeeded with model {model}")
                for log in EventLogger().log(response):
                    log.print()
                
                successful_queries += 1
                
            except Exception as e:
                self.logger.error(f"Query {i} failed with model {model}: {e}")
                pytest.fail(f"Query execution failed: {e}")
        
        # Print number of successful queries
        self.logger.info(f"Successfully completed {successful_queries} out of {len(queries)} queries with model {model}")
        
        # All queries should have succeeded
        assert successful_queries == len(queries)


# Conftest.py content for better reporting
def pytest_html_report_title(report):
    """Set the title of the HTML report."""
    report.title = "MCP Server Test Report"


def pytest_configure(config):
    """Add metadata to pytest HTML report."""
    config._metadata['Project'] = 'MCP Server Testing'
    config._metadata['Testing Date'] = '2025-04-09'
