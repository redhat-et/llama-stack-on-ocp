import threading
from typing import List, Optional, Union, Callable, Any
from urllib.parse import urlparse

from llama_stack_client import LlamaStackClient, Agent
from llama_stack_client.lib.agents.client_tool import ClientTool
from llama_stack_client.lib.agents.tool_parser import ToolParser
from llama_stack_client.types import SamplingParams, ResponseFormat
from llama_stack_client.types.shared_params.agent_config import Toolgroup, ToolConfig
from pydantic import BaseModel, model_validator

from common.server import A2AServer
from common.types import AgentCard
from demos.a2a_llama_stack.A2ATool import A2ATool
from demos.a2a_llama_stack.task_manager import AgentTaskManager


class LLSAgentConfiguration(BaseModel):
    tool_parser: Optional[ToolParser] = None,
    model: Optional[str] = None,
    instructions: Optional[str] = None,
    tools: Optional[List[Union[Toolgroup, ClientTool, Callable[..., Any]]]] = None,
    tool_config: Optional[ToolConfig] = None,
    sampling_params: Optional[SamplingParams] = None,
    max_infer_iters: Optional[int] = None,
    input_shields: Optional[List[str]] = None,
    output_shields: Optional[List[str]] = None,
    response_format: Optional[ResponseFormat] = None,
    enable_session_persistence: Optional[bool] = None,


class AgentSpecification(BaseModel):
    a2a_agent_card: AgentCard | None
    lls_agent_config: LLSAgentConfiguration | None
    url: str | None
    managed: bool = True

    @model_validator(mode='after')
    def validate_specification(self):
        if self.a2a_agent_card is None and self.url is None:
            raise ValueError("Either the agent URL or the agent A2A card must be provided.")
        if self.a2a_agent_card is not None and self.url is None:
            self.url = self.a2a_agent_card.url
        if self.managed:
            if self.a2a_agent_card is None:
                raise ValueError("The agent A2A card must be provided for a managed agent.")
            if self.lls_agent_config is None:
                raise ValueError("The Llama Stack agent configuration must be provided for a managed agent.")
            parsed_url = urlparse(self.url)
            if parsed_url.hostname not in ('localhost', '127.0.0.1'):
                raise ValueError("Cannot run A2A server on a remote host.")

        return self


class A2AFleetAgent:
    def __init__(self, agent_specification: AgentSpecification):
        self.spec = agent_specification
        self.client_tool_method = A2ATool(self.spec.url, self.spec.a2a_agent_card)

        # after the client tool initialization, we have the agent card even if it was not given at init
        self.spec.a2a_agent_card = self.client_tool_method.agent_card

        # if this is a managed agent, the LLS agent object and the A2A server wrapper will be initialized later
        self.lls_agent = None
        self.a2a_server = None

    def run_agent(self, client: LlamaStackClient):
        if not self.spec.managed:
            return

        self.lls_agent = Agent(client=client, **self.spec.lls_agent_config.dict())

        task_manager = AgentTaskManager(agent=self.lls_agent)
        parsed_url = urlparse(self.spec.url)
        self.a2a_server = A2AServer(
            agent_card=self.spec.a2a_agent_card,
            task_manager=task_manager,
            host='localhost',
            port=parsed_url.port
        )
        thread = threading.Thread(target=self.a2a_server.start, daemon=True)
        thread.start()


class A2AFleet:
    """
    A manager for a set of A2A-aware Llama Stack agents.
    """
    def __init__(self, llama_stack_url: str, agent_specs: List[AgentSpecification]):
        self.client = LlamaStackClient(base_url=llama_stack_url)

        self.agents = {}
        for spec in agent_specs:
            agent = A2AFleetAgent(agent_specification=spec)
            agent_id = agent.spec.a2a_agent_card.name
            self.agents[agent_id] = agent

        self.fleet_active = False

    def run_fleet(self):
        """
        Initialize the managed Llama Stack servers and run each of them as a dedicated A2A server.
        """
        for agent in self.agents.values():
            agent.run_agent(self.client)
        self.fleet_active = True

    def query_agent(self, agent_id, **kwargs):
        """
        Send a query to a managed Llama Stack agent.
        TODO: this way to access an agent is not thread-safe!
        """
        if not self.fleet_active:
            raise Exception("The fleet is not yet active.")
        if agent_id not in self.agents:
            raise ValueError(f"Unknown agent ID: {agent_id}")
        agent = self.agents[agent_id]
        if not agent.spec.managed:
            raise ValueError(f"Agent {agent_id} is an external A2A agent and cannot be queried via this interface.")
        agent.lls_agent.create_turn(**kwargs)


class FullMeshA2AFleet(A2AFleet):
    """
    Manages a set of A2A agents where all participating agents, apart from the external ones, are aware of each other.
    """
    def run_fleet(self):
        # before actually running the agents, modify their tool lists to include the peer client methods
        for agent in self.agents.values():
            if not agent.spec.managed:
                continue
            client_tools = [a.client_tool_method for a in self.agents.values() if a != agent]
            if not client_tools:
                continue
            if agent.spec.lls_agent_config.tools is None:
                agent.spec.lls_agent_config.tools = []
            agent.spec.lls_agent_config.tools.extend(client_tools)

        super().run_fleet()


class RouterAgentA2AFleet(A2AFleet):
    """
    Uses a dedicated router agent to redirect incoming requests to agents based on their capabilities
    """
    pass  # TODO
