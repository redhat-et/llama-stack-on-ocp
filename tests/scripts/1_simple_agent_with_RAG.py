# Code bellow written following examples here: https://llama-stack.readthedocs.io/en/latest/building_applications
# Code bellow written following examples here: https://llama-stack.readthedocs.io/en/latest/building_applications/rag.html
from llama_stack_client.lib.agents.agent import Agent
from llama_stack_client.lib.agents.event_logger import EventLogger
from llama_stack_client.types import Document

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
parser.add_argument("-a", "--auto", help="Automatically runs examples, and does not start a chat session", action="store_true")
args = parser.parse_args()

model="meta-llama/Llama-3.2-3B-Instruct"

# Connect to a llama stack server
if args.remote:
    base_url = os.getenv("REMOTE_BASE_URL")
    mcp_url = os.getenv("REMOTE_MCP_URL")
    vdb_provider = os.getenv("REMOTE_VDB_PROVIDER")
else:
    base_url="http://localhost:8321"
    mcp_url="http://host.containers.internal:8000/sse"
    vdb_provider="faiss"

client = LlamaStackClient(base_url=base_url)
logger.info(f"Connected to Llama Stack server @ {base_url} \n")

# Get tool info and register tools
registered_tools = client.tools.list()
registered_tools_identifiers = [t.identifier for t in registered_tools]
registered_toolgroups = [t.toolgroup_id for t in registered_tools]

if "mcp::custom_tool" not in registered_toolgroups:
    # Register MCP tools
    client.toolgroups.register(
        toolgroup_id="mcp::custom_tool",
        provider_id="model-context-protocol",
        mcp_endpoint={"uri":mcp_url},
        )
mcp_tools = [t.identifier for t in client.tools.list(toolgroup_id="mcp::custom_tool")]

vector_db_ids = [vector_db.provider_resource_id for vector_db in client.vector_dbs.list()]
if "my_documents" not in vector_db_ids:
    response = client.vector_dbs.register(
    vector_db_id="my_documents",
    embedding_model="all-MiniLM-L6-v2",
    embedding_dimension=384,
    provider_id=vdb_provider,
    )

    urls = ["https://raw.githubusercontent.com/meta-llama/llama-stack/refs/heads/main/README.md"]
    documents = [
        Document(
            document_id=f"num-{i}",
            content=doc,
            mime_type="text/pain",
            metadata={},
        ) for i, doc in enumerate(urls)
        ]

    client.tool_runtime.rag_tool.insert(
    documents=documents,
    vector_db_id="my_documents",
    chunk_size_in_tokens=512,
)


logger.info(f"""Your Server has access the the following toolgroups:
{set(registered_toolgroups)}
""")

# Create simple agent with tools
agent = Agent(
    client,
    model=model,
    instructions = """You are a helpful assistant. You have access to a number of tools.
    Whenever a tool is called, be sure return the Response in a friendly and helpful tone.
    When you are asked to search the web you must use a tool.
    """ ,
    tools=["mcp::custom_tool",{
        "name":"builtin::rag",
            "args":{
                "vector_db_ids":["my_documents"],
                "top_k": 1,
                }
    }
    ],
    tool_config={"tool_choice":"auto"}
)

if args.auto:
    user_prompts = ["""Please use the knowledge search tool to tell me what you know about Llama Stack.""",
                    """Give me a random number between 1 and 1010."""]
    session_id = agent.create_session(session_name="Auto_demo")
    for prompt in user_prompts:
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
        for log in EventLogger().log(turn_response):
            log.print()

else:
    #Create a chat session
    session_id = agent.create_session(session_name="Conversation_demo")
    while True:
        user_input = input(">>> ")
        if "/bye" in user_input:
            if args.session_info_on_exit:
                agent_session = client.agents.session.retrieve(session_id=session_id, agent_id=agent.agent_id)
                print( agent_session.to_dict())
            break
        turn_response = agent.create_turn(
            session_id=session_id,
            messages=[{"role": "user", "content": user_input}],
        )

        for log in EventLogger().log(turn_response):
            log.print()
