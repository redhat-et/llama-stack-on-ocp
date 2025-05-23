import os
import logging

from llama_stack_client import LlamaStackClient, Agent

from common.server import A2AServer
from common.types import AgentCard, AgentCapabilities, AgentSkill

from .task_manager import AgentTaskManager, SUPPORTED_CONTENT_TYPES

logging.basicConfig(level=logging.INFO)


def build_server(host: str = "0.0.0.0", port: int = 10010):
    # 1) instantiate your agent with the required parameters
    agent = Agent(
        client=LlamaStackClient(base_url=os.getenv("REMOTE_BASE_URL", "http://localhost:8321")),
        model=os.getenv("INFERENCE_MODEL_ID", "llama3.1:8b-instruct-fp16"),
        instructions="You are an orchestration assistant. Ensure you count correctly the number of skills needed.",
        max_infer_iters=10,
        sampling_params = {
                    "strategy": {"type": "greedy"},
                    "max_tokens": 4096,
                },
    )

    # 2) wrap it in the A2A TaskManager
    task_manager = AgentTaskManager(agent=agent, internal_session_id=True)

    # 3) advertise your tools as AgentSkills
    card = AgentCard(
        name="Orchestration Agent",
        description="Plans which tool to call for each user question",
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
            id="orchestrate",
            name="Orchestration Planner",
            description="Plan user questions into JSON steps of {skill_id}",
            tags=["orchestration"],
            examples=["Plan: What's today's date and a random number?"],
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
