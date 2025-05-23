import os
import logging

from llama_stack_client import LlamaStackClient, Agent

from common.server import A2AServer
from common.types import AgentCard, AgentCapabilities, AgentSkill

from .task_manager import AgentTaskManager, SUPPORTED_CONTENT_TYPES

logging.basicConfig(level=logging.INFO)


def build_server(host: str = "0.0.0.0", port: int = 10012):
    # 1) instantiate your agent with the required parameters
    agent = Agent(
        client=LlamaStackClient(base_url=os.getenv("REMOTE_BASE_URL", "http://localhost:8321")),
        model=os.getenv("INFERENCE_MODEL_ID", "llama3.2:3b-instruct-fp16"),
        instructions=("You are skilled at writing human-friendly text based on the query and associated skills."),
        max_infer_iters=3,
        sampling_params = {
                    "strategy": {"type": "greedy"},
                    "max_tokens": 4096,
                },
    )

    # 2) wrap it in the A2A TaskManager
    task_manager = AgentTaskManager(agent=agent, internal_session_id=True)

    # 3) advertise your tools as AgentSkills
    card = AgentCard(
        name="Writing Agent",
        description="Generate human-friendly text based on the query and associated skills",
        url=f"http://{host}:{port}/",
        version="0.1.0",
        defaultInputModes=["text/plain"],
        defaultOutputModes=SUPPORTED_CONTENT_TYPES,
        capabilities=AgentCapabilities(
            streaming=False,
            pushNotifications=False,
            stateTransitionHistory=False,
            ),
    skills = [
        AgentSkill(
            id="writing_agent",
            name="Writing Agent",
            description="Write human-friendly text based on the query and associated skills",
            tags=["writing"],
            examples=["Write human-friendly text based on the query and associated skills"],
            inputModes=["text/plain"],
            outputModes=["application/json"],
            )
        ]
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
