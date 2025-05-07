import os
import logging
from common.server import A2AServer
from common.types import AgentCard, AgentCapabilities, AgentSkill

from .agent import MyCustomAgent
from .task_manager import AgentTaskManager

logging.basicConfig(level=logging.INFO)

def build_server(host: str = "0.0.0.0", port: int = 10010):
    # 1) instantiate your agent with the required parameters
    agent = MyCustomAgent(
        base_url=os.getenv("LLAMA_STACK_URL", "http://localhost:8321"),
        model_id=os.getenv("MODEL_ID", "llama3.2:3b-instruct-fp16"),
    )

    # 2) wrap it in the A2A TaskManager
    task_manager = AgentTaskManager(agent=agent)

    # 3) advertise your tools as AgentSkills
    card = AgentCard(
        name="Custom Agent",
        description="Generates random numbers or dates",
        url=f"http://{host}:{port}/",
        version="0.1.0",
        defaultInputModes=["text/plain"],
        defaultOutputModes=MyCustomAgent.SUPPORTED_CONTENT_TYPES,
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
