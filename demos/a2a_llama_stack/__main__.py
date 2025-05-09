import os
import logging

from llama_stack_client import LlamaStackClient, Agent

from common.server import A2AServer
from common.types import AgentCard, AgentCapabilities, AgentSkill

from .agent import random_number_tool, date_tool
from .task_manager import AgentTaskManager, SUPPORTED_CONTENT_TYPES

logging.basicConfig(level=logging.INFO)


def build_server(host: str = "0.0.0.0", port: int = 10010):
    # 1) instantiate your agent with the required parameters
    agent = Agent(
        client=LlamaStackClient(base_url=os.getenv("LLAMA_STACK_URL", "http://localhost:8321")),
        model=os.getenv("MODEL_ID", "llama3.2:3b-instruct-fp16"),
        instructions=(
            "You have access to two tools:\n"
            "- random_number_tool: generates a random integer between 1 and 100\n"
            "- date_tool: returns today's date in YYYY-MM-DD format\n"
            "Use the appropriate tool to answer user queries."
        ),
        tools=[random_number_tool, date_tool],
        max_infer_iters=3,
    )

    # 2) wrap it in the A2A TaskManager
    task_manager = AgentTaskManager(agent=agent, internal_session_id=True)

    # 3) advertise your tools as AgentSkills
    card = AgentCard(
        name="Custom Agent",
        description="Generates random numbers or dates",
        url=f"http://{host}:{port}/",
        version="0.1.0",
        defaultInputModes=["text/plain"],
        defaultOutputModes=SUPPORTED_CONTENT_TYPES,
        capabilities=AgentCapabilities(streaming=True),
        skills=[
            AgentSkill(id="random_number", name="Random Number Generator"),
            AgentSkill(id="get_date",      name="Date Provider"),
        ],
    )

    return A2AServer(
        agent_card=card,
        task_manager=task_manager,
        host=host,
        port=port,
    )

if __name__ == "__main__":
    import click

    @click.command()
    @click.option("--host", default="0.0.0.0")
    @click.option("--port", default=10010, type=int)
    def main(host, port):
        build_server(host, port).start()

    main()
