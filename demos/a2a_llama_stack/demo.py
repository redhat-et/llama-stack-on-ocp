import os
import threading

from llama_stack_client import Agent, LlamaStackClient
from llama_stack_client.lib.agents.event_logger import EventLogger
from termcolor import cprint

from common.server import A2AServer
from common.types import AgentCard, AgentSkill, AgentCapabilities
from demos.a2a_llama_stack.A2ATool import A2ATool
from demos.a2a_llama_stack.agent import random_number_tool
from demos.a2a_llama_stack.task_manager import AgentTaskManager

EXTERNAL_AGENT_LOCAL_PORT = 8080


def run_external_agent():
    agent_url = f"http://localhost:{EXTERNAL_AGENT_LOCAL_PORT}"

    lls_agent = Agent(
        client=LlamaStackClient(base_url=os.getenv("LLAMA_STACK_URL", "http://localhost:8321")),
        model=os.getenv("MODEL_ID", "meta-llama/Llama-3.1-8B-Instruct"),
        instructions="You are an expert in generating random numbers. When asked, only answer with the number.",
    )

    agent_card = AgentCard(
        name="Random Number Generator",
        description="Generates random numbers",
        url=agent_url,
        version="0.1.0",
        defaultInputModes=["text/plain"],
        defaultOutputModes=["text/plain"],
        capabilities=AgentCapabilities(streaming=True),
        skills=[
            AgentSkill(id="random_number", name="Random Number Generator"),
        ],
    )
    task_manager = AgentTaskManager(agent=lls_agent)
    server = A2AServer(
        agent_card=agent_card,
        task_manager=task_manager,
        host='localhost',
        port=EXTERNAL_AGENT_LOCAL_PORT
    )
    thread = threading.Thread(target=server.start, daemon=True)
    thread.start()

    return agent_url


def external_agent_as_a_tool():
    print(f"Launching tool agent on port {EXTERNAL_AGENT_LOCAL_PORT}...")
    external_agent_url = run_external_agent()

    print("Connecting tool agent to the main agent...")
    external_agent_tool = A2ATool(external_agent_url)
    agent = Agent(
        client=LlamaStackClient(base_url=os.getenv("LLAMA_STACK_URL", "http://localhost:8321")),
        model=os.getenv("MODEL_ID", "granite32-8b"),
        instructions="You are a helpful assistant. When a tool is used, only print its output without adding more content.",
        tools=[external_agent_tool],
    )
    session_id = agent.create_session("test-session")

    prompt = "Generate a random number between 1 and 10."
    cprint(f"User> {prompt}", "green")
    response = agent.create_turn(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        session_id=session_id,
    )
    for log in EventLogger().log(response):
        log.print()


if __name__ == '__main__':
    external_agent_as_a_tool()
