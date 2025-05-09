# Code bellow written following examples here: https://llama-stack.readthedocs.io/en/latest/building_applications
from llama_stack_client import Agent
from llama_stack_client.lib.agents.event_logger import EventLogger
from llama_stack_client import LlamaStackClient
from termcolor import cprint
import argparse
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


parser = argparse.ArgumentParser()
parser.add_argument("-r", "--remote", help="Uses the remote_url", action="store_true")
parser.add_argument("-s", "--session-info-on-exit", help="Prints agent session info on exit", action="store_true")
parser.add_argument("-m", "--model", type=str, choices=["llama","granite"], required=True, help="Uses a specific model to run (llama or granite)")
args = parser.parse_args()

# Connect to a llama stack server
if args.remote:
    base_url = os.getenv("REMOTE_BASE_URL")
    slack_mcp_url = os.getenv("REMOTE_SLACK_MCP_URL")
    ocp_mcp_url = os.getenv("REMOTE_OCP_MCP_URL")
else:
    base_url="http://localhost:8321"
    slack_mcp_url="http://host.containers.internal:8000/sse"
    ocp_mcp_url="http://host.containers.internal:8000/sse"

client = LlamaStackClient(base_url=base_url)
logger.info(f"Connected to Llama Stack server @ {base_url} \n")

# Get tool info and register tools
registered_tools = client.tools.list()
registered_tools_identifiers = [t.identifier for t in registered_tools]
registered_toolgroups = [t.toolgroup_id for t in registered_tools]

# check if the slack mcp server is registered
if "mcp::slack" not in registered_toolgroups:
    # Register MCP tools
    client.toolgroups.register(
        toolgroup_id="mcp::slack",
        provider_id="model-context-protocol",
        mcp_endpoint={"uri":slack_mcp_url},
        )
mcp_tools_slack = [t.identifier for t in client.tools.list(toolgroup_id="mcp::slack")]

# check if the openshift mcp server is registered
if "mcp::openshift" not in registered_toolgroups:
    # Register MCP tools
    client.toolgroups.register(
        toolgroup_id="mcp::openshift",
        provider_id="model-context-protocol",
        mcp_endpoint={"uri":ocp_mcp_url},
        )
mcp_tools_ocp = [t.identifier for t in client.tools.list(toolgroup_id="mcp::openshift")]

logger.info(f"""Your Server has access the the following toolgroups:
{set(registered_toolgroups)}
""")

# setting the model names
llama_model="meta-llama/Llama-3.2-3B-Instruct"
granite_model="ibm-granite/granite-3.2-8b-instruct"
# system prompts for different models
llama_prompt = """You are a helpful assistant. You have access to a number of tools.
    Whenever a tool is called, be sure return the Response in a friendly and helpful tone.
    When you are asked to search the web you must use a tool."""
granite_prompt = """You are a helpful AI assistant with access to the tools listed next. When a tool is required to answer the user's query, respond with `<tool_call>` followed by a JSON object of the tool used. For example: `<tool_call> {"name":"function_name","arguments":{"arg1":"value"}} </tool_call>`:The user will respond with the output of the tool execution response so you can continue with the rest of the initial user prompt (continue).
If a tool does not exist in the provided list of tools, notify the user that you do not have the ability to fulfill the request."""

# Create simple agent with tools
if args.model not in ["llama", "granite"]:
     print("Unsupported model. Please choose either 'llama' or 'granite'.")
if args.model == "llama":
    agent = Agent(
        client,
        model=llama_model,
        instructions = llama_prompt,
        tools=["mcp::slack", "mcp::openshift"],
        tool_config={"tool_choice":"auto"},
        sampling_params={"max_tokens":4096, "strategy":{"type": "greedy"},}
    )
elif args.model == "granite":
        agent = Agent(
        client,
        model=granite_model,
        instructions = granite_prompt,
        tools=["mcp::slack", "mcp::openshift"],
        tool_config={"tool_choice":"auto"},
        sampling_params={"max_tokens":4096, "strategy":{"type": "greedy"},}
    )

user_prompts = ["""View the logs for pod test-pod in the llama-serve OpenShift namespace. Categorize it as normal or error.""",
                """Summarize the results with the pod name, category along with a briefly explaination as to why you categorized it as normal or error. Respond with plain text only. Do not wrap your response in additional quotation marks.""",
                """Send a message with the summarization to the demos channel on Slack."""]
session_id = agent.create_session(session_name="Slack_OCP_MCP_demo")
for i, prompt in enumerate(user_prompts):
    turn_response = agent.create_turn(
        messages=[
            {
                "role":"user",
                "content": prompt
            }
        ],
        session_id=session_id,
        stream=True,
    )
    print("============ Turn: ", i, "========")
    for log in EventLogger().log(turn_response):
        log.print()
