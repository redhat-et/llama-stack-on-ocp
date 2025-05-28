import os
import logging
import importlib
import click

from llama_stack_client import LlamaStackClient, Agent
from common.server import A2AServer
from common.types import AgentCard, AgentCapabilities, AgentSkill

logging.basicConfig(level=logging.INFO)

def build_server(agent_name: str, host: str, port: int = None):
    try:
        config_module_path = f"{__package__}.agents.{agent_name.replace('-', '_')}.config"
        config_module = importlib.import_module(config_module_path)
        agent_config_data = config_module.AGENT_CONFIG
    except ModuleNotFoundError:
        logging.error(f"Configuration module not found for agent: {agent_name} at {config_module_path}")
        raise
    except AttributeError:
        logging.error(f"AGENT_CONFIG not found in {config_module_path}")
        raise

    if port is None:
        port = agent_config_data.get("default_port", 8000)

    agent_params_config = agent_config_data["agent_params"]
    tools_to_pass = agent_params_config.get("tools", [])

    agent = Agent(
        client=LlamaStackClient(base_url=os.getenv("REMOTE_BASE_URL", "http://localhost:8321")),
        model=os.getenv(agent_params_config["model_env_var"], agent_params_config["default_model"]),
        instructions=agent_params_config["instructions"],
        tools=tools_to_pass,
        max_infer_iters=agent_params_config.get("max_infer_iters", 3),
        sampling_params=agent_params_config.get("sampling_params", None)
    )

    TaskManagerClass = agent_config_data["task_manager_class"]
    task_manager = TaskManagerClass(agent=agent, internal_session_id=True)

    card_params_config = agent_config_data["agent_card_params"]
    agent_skills = [AgentSkill(**skill_p) for skill_p in card_params_config.get("skills_params", [])]
    capabilities = AgentCapabilities(**card_params_config.get("capabilities_params", {}))

    card = AgentCard(
        name=card_params_config["name"],
        description=card_params_config["description"],
        url=f"http://{host}:{port}/",
        version=card_params_config.get("version", "0.1.0"),
        defaultInputModes=card_params_config.get("default_input_modes", ["text/plain"]),
        defaultOutputModes=card_params_config.get("default_output_modes", ["text/plain"]),
        capabilities=capabilities,
        skills=agent_skills
    )

    return A2AServer(
        agent_card=card,
        task_manager=task_manager,
        host=host,
        port=port,
    )

@click.command()
@click.option("--agent-name", required=True, help="The name of the agent to run (e.g., a2a_planner, a2a_custom_tools). Corresponds to the directory name.")
@click.option("--host", default="0.0.0.0", help="Host to bind the server to.")
@click.option("--port", type=int, default=None, help="Port to bind the server to (overrides agent's default).")
def main(agent_name, host, port):
    effective_port = port
    if port is None:
        try:
            config_module_path = f"agents.a2a_llama_stack.agents.{agent_name.replace('-', '_')}.config"
            config_module = importlib.import_module(config_module_path)
            effective_port = config_module.AGENT_CONFIG.get("default_port", "config_default")
        except Exception:
            effective_port = "unknown_default"


    logging.info(f"Attempting to start server for agent: {agent_name} on {host}:{effective_port}")
    server = build_server(agent_name=agent_name, host=host, port=port)
    server.start()
    logging.info(f"Server for agent {agent_name} should be running.")


if __name__ == "__main__":
    main()
