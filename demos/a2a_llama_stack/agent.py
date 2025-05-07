import random
from datetime import datetime
from llama_stack_client import LlamaStackClient, Agent, AgentEventLogger
from typing import AsyncIterator, Iterator


def random_number_tool() -> int:
    """
    Generate a random integer between 1 and 100.
    """
    print("\n\nGenerating a random number...\n\n")
    return random.randint(1, 100)


def date_tool() -> str:
    """
    Return today's date in YYYY-MM-DD format.
    """
    return datetime.utcnow().date().isoformat()


class MyCustomAgent:
    """
    A custom agent leveraging Llama Stack's built-in tool routing to
    automatically select and execute registered tools.
    """
    SUPPORTED_CONTENT_TYPES = ["text", "text/plain", "application/json"]

    def __init__(self, base_url: str, model_id: str):
        # Initialize the Llama Stack client
        self.client = LlamaStackClient(base_url=base_url)

        # Create an Agent with our custom tools; name/description are inferred by the service
        self.agent = Agent(
            client=self.client,
            model=model_id,
            instructions=(
                "You have access to two tools:\n"
                "- random_number_tool: generates a random integer between 1 and 100\n"
                "- date_tool: returns today's date in YYYY-MM-DD format\n"
                "Use the appropriate tool to answer user queries."
            ),
            tools=[random_number_tool, date_tool],
            max_infer_iters=3,
        )

        # Create or retrieve a session; returns a session ID string
        self.session_id = self.agent.create_session("custom-agent-session")

    def invoke(self, query: str, session_id: str) -> str:
        """
        Route the user query through the Agent, executing tools as needed.
        """
        # Determine which session to use
        # Always use the internally managed session
        sid = self.session_id

        # Send the user query to the Agent
        turn_resp = self.agent.create_turn(
            messages=[{"role": "user", "content": query}],
            session_id=sid,
        )

        # Extract tool and LLM outputs from events
        logs = AgentEventLogger().log(turn_resp)
        output = ""
        for event in logs:
            if hasattr(event, "content") and event.content:
                output += event.content
        return output

    async def stream(self, query: str, session_id: str) -> AsyncIterator[dict]:
        """
        Simplest streaming stub: synchronously invoke and emit once.
        """
        result = self.invoke(query, session_id)
        yield {"updates": result, "is_task_complete": True, "content": result}
