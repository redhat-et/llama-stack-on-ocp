# Streamlit UI for Llama Stack

## Introduction
This Streamlit web app is an alternative to [demo notebooks](/demos/rag_agentic/notebooks). It showcases RAG and agentic agents built with Llama Stack.

This tools playground is directly built on top of the [llama-stack playground](https://llama-stack.readthedocs.io/en/latest/playground/index.html). It aims to:
* Showcase tool calling via built-in tools and MCP servers with Llama Stack in an interactive environment
* Showcase ReAct agent with Llama Stack and its capability with tool calling
* Provide an UI to help users inspect and understand Llama Stack API providers and resources

This folder consists of a [Containerfile](/demos/rag_agentic/frontend/build/Containerfile) that can be used to build your own Streamlit image. You can then deploy Streamlit in your OpenShift env by referring to the [Streamlit deployment on OpenShift guide](https://github.com/opendatahub-io/llama-stack-demos/tree/main/kubernetes/streamlit-client).

## Key Features

### Speak with an agent for tool calling.
In the example below, a llama-stack agent is able to perform a tool call via one of its built-in tools, e.g. websearch through brave search to locate where the Red Hat Summit 2025 is taking place.

![tools_normal_agent_websearch](/images/tools_normal_agent_websearch.gif)

### Leverage ReAct Prompting for advanced use case
In the example below, a llama-stack agent is able to configure through [ReAct prompting](https://react-lm.github.io/) and call multi tools through different steps. The agent is able to search the result of the recent 2025 Boston Marathon and return the result to the given slack channel.

![tools_react_agent_websearch_slackmcp](/images/tools_react_agent_websearch_slackmcp.gif)

The results from the slack channel could be found below.
![boston_marathon_slack_result](/images/boston_marathon_slack_result.png)

### Dynamically Register MCP Servers
To use the MCP servers, please refer to these existing [MCP servers for Llama Stack](https://github.com/opendatahub-io/llama-stack-demos/tree/main/kubernetes/mcp-servers).

Once the MCP servers are registered (e.g., on OpenShift), they should be automatically discovered and displayed in the Streamlit Web App environment, allowing the agent to use their tools.

## Run the Streamlit UI for Llama Stack
To replicate this Streamlit Web App on tool calling with Llama stack, please follow the instructions below.

### Step 1: Install and setup
#### Setup Web Search API
First, we want to export the API key for the web search tool (Tavily) into our environment.

`export TAVILY_SEARCH_API_KEY=tvly-...`.

Then we will deploy the Llama Stack server remotely via OpenShift or locally via Ollama.

#### Option 1: Setup Llama Stack server on an OpenShift Container

For remote inference, setup your Llama Stack Server on an OpenShift Container Platform following this [deployment guide](https://github.com/opendatahub-io/llama-stack-demos/tree/main/kubernetes/streamlit-client), then export the endpoint:

`export LLAMA_STACK_ENDPOINT="http://llamastack-deployment-llama-serve.apps.ocp-beta-test.nerc.mghpcc.org:80"`

#### Option 2: Setup Llama Stack server via Ollama
First, install [uv](https://docs.astral.sh/uv/getting-started/installation/) for package management.

For local inference:
* Install [Ollama](https://ollama.com/download).
* Run the desired Ollama model, keeping it alive:

`ollama run llama3.2:3b --keepalive 60m`

* Use `uv` to run the Llama Stack backend server, connecting it to your Ollama model:

`INFERENCE_MODEL=llama3.2:3b uv run --with llama-stack llama stack build --template ollama --image-type venv --run`

### Step 2: Run the demo

#### Option 1: Setup Streamlit Web App remotely through OpenShift

Now, deploy your demo using this [containerfile](https://github.com/opendatahub-io/llama-stack-demos/blob/main/demos/rag_agentic/frontend/build/Containerfile). This container builds the Streamlit frontend application. It fetches a version of the upstream Llama Stack distribution where the Streamlit Web App source code can be accessed at: [playground/tools.py](https://github.com/meta-llama/llama-stack/blob/main/llama_stack/distribution/ui/page/playground/tools.py).

After the deployment is complete and the route is exposed, you can access the Tools Playground Web App at the provided URL (typically using the default Streamlit port 8501 within the container).

#### Option 2: Setup Streamlit Web App locally

If you deployed the Llama Stack server locally (Step 1, Option 2), run the Streamlit frontend application:

`streamlit run llama_stack/distribution/ui/app.py`

This command starts the web interface, which connects to the backend server started in Step 1. The web app's source code can be found at [playground/tools.py](https://github.com/meta-llama/llama-stack/blob/main/llama_stack/distribution/ui/page/playground/tools.py).
