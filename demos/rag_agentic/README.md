# RAG/Agentic/MCP Demo

## Try Out Llama Stack Tool Calling and RAG Agents!

Once your llama stack server is up and running you can deploy the llama stack playground to quickly test out interacting with agents that have access to tools, mcp servers and vectorDB's.

To deploy the playground locally, first build the ui image from the root directory using the provided [Makefile](../../Makefile).

```bash
make build_ui
```
Followed by setting the correct environment variables (*note: TAVILY_SEARCH_API_KEY is only needed for the web search tool and can be skipped if you do not intend to use that tool*).

```bash
export LLAMA_STACK_ENDPOINT=****
export TAVILY_SEARCH_API_KEY=****
make run_ui
```

Once the pod starts, you can open your browser and go to `http://localhost:8501`. There you will find the interactive llama stack playground shown below.


<div style="text-align: center;">
<img src="../../images/playground-tools-page.png" width="70%" height="70%">
</div>

## Deep Dive into Implementing Llama Stack Tool Calling and RAG Agents!

If you would like to learn more about how to implement your own agents with Llama Stack, this demo directory offers a practical learning path for anyone interested in understanding and gaining hands-on experience with LlamaStack and AI agents. The notebooks are structured progressively, starting from foundational concepts and gradually advancing to more complex implementations, helping users build the skills needed to develop AI-powered applications!

1. **Level 1**: Understand foundational RAG concepts (Low difficulty)
2. **Level 2**: Try out simple agentic demo with single tool ussage. (Medium-low difficulty)
3. **Level 3**: Try out simple agentic demo with single tool ussage. (Medium difficulty)
4. **Level 4**: Combine RAG with agentic capabilities (Medium difficulty)
5. **Level 5**: Explore advanced agentic + MCP (model context protocol) examples (Medium difficulty)
6. **Level 6**: Explore advanced agentic + MCP + RAG examples (Medium difficulty)


### Folder Structure
- [`notebooks/`](notebooks/): Jupyter notebooks for learning RAG and agent implementation
- [`src/`](src/): Python source files for production implementation
- [`frontend/`](frontend/): Containerfile for building the streamlit UI.

### Getting Started
### 1. [`notebooks/`](notebooks/): Start with notebooks in order
- [Level1_foundational_RAG.ipynb](notebooks/Level1_foundational_RAG.ipynb): Start here! Learn the basics of RAG.
- [Level2_simple_agentic_with_websearch.ipynb](notebooks/Level2_simple_agentic_with_websearch.ipynb): Add web search capabilities to your agent.
- [Level3_advance_agentic_with_Prompt_Chaining_ReAct.ipynb](notebooks/Level3_advance_agentic_with_Prompt_Chaining_ReAct.ipynb): Advanced Agentic capabilities with prompt chaining and ReAct Agent.
- [Level4_agentic_RAG.ipynb](notebooks/Level4_agentic_RAG.ipynb): Agentic RAG example, combining RAG with agentic capabilities.
- [Level5_agentic_and_mcp.ipynb](notebooks/Level5_agentic_and_mcp.ipynb): Advanced topics in agentic and MCP, showcasing  sequential tool calls and conditional logic within an agentic workflow.
- [Level6_agentic_MCP_and_RAG.ipynb](notebooks/Level6_agentic_MCP_and_RAG.ipynb): Advanced Agentic, RAG, MCP example, showcasing how RAG can be incorporated into sequential tool calls.

#### 2. Review source code in [`src/`](src/)
Contains Python source files that implement the concepts from the notebooks. Good for future production stage.
Before running scripts, remember to set up your environment variables using [.env.example](src/.env.example) as a template

#### 3. Deploy and play with [`frontend/`](frontend/) Streamlit UI
This folder contains the containerfile to build a user interface based on the playground UI provided by llama-stack. The playground UI is a Streamlit application that provides an interactive interface for testing and experimenting with language models.
For more information, visit: https://llama-stack.readthedocs.io/en/latest/playground

# Demo Scenario: Building an Intelligent Operations Agent for our OpenShift Clusters at Parasol Insurance

Our operations team faces the challenges of managing a growing number of OpenShift clusters, often dealing with fragmented documentation, recurring incidents, and the need for repetitive troubleshooting. To alleviate cognitive overload and accelerate incident response, we are developing an advanced agent that integrates Retrieval-Augmented Generation (RAG) for knowledge retrieval, OpenShift control via a Model Context Protocol (MCP), and communication through Slack.

**Product Vision:**

This agent aims to provide:

* **Intelligent Chat Functionality:** Leveraging Large Language Models (LLMs) for natural language interaction.
* **Internal Knowledge Search (RAG):** Accessing and synthesizing information from our internal documentation for efficient troubleshooting.
* **External Knowledge Augmentation:** Searching external resources to supplement internal knowledge.
* **Proactive Hazard Prediction:** Integrating weather forecasts to anticipate potential infrastructure disruptions.
* **OpenShift Interaction (Agent + MCP):** Executing commands and gathering information directly from our OpenShift clusters.
* **Automated Incident Response:** Analyzing OpenShift pod logs, retrieving relevant solutions via RAG, summarizing the issue, and communicating updates via Slack (MCP).

We are building this agent through a series of focused demonstrations, each progressively adding more sophisticated capabilities. The following notebooks illustrate this incremental development:

## Notebook Overview

1.  **`Level1_foundational_RAG.ipynb`:**
    * **Focus:** Demonstrates the foundational RAG component, showcasing how to use llama stack to retrieve information from our internal knowledge base to answer queries.
    * **Task Example:** Explain how to install Openshift using the guide pdf.
    * **Agent Capability:** Uses `RAG` to retrieve and summarize the internal document.

2.  **`Level2_simple_agentic_with_websearch.ipynb`:**
    * **Focus:** Introduces the basic agent framework with the ability to utilize tools. This notebook showcases the agent's capacity to interact with the external world.
    * **Task Example:** What’s latest in OpenShift?
    * **Agent Capability:** Uses a `web_search_tool` to retrieve and summarize publicly available information.

3.  **`Level3_advance_agentic_with_Prompt_Chaining_ReAct.ipynb`:**
    * **Focus:** Builds upon the simple agent by incorporating location awareness, prompt chaining for complex reasoning, and the ReAct framework for structured action planning.
    * **Task Example:** "Hey, check if there’s anything happening weather-wise near me that might affect our pod deployments." / "Are there any weather-related risks in my area that could disrupt network connectivity or system availability?"
    * **Agent Capabilities:** Utilizes a `web_search_tool` for weather information and a `get_location` client tool. Demonstrates prompt chaining and the ReAct agent methodology.

4.  **`Level4_agentic_RAG.ipynb`:**
    * **Focus:** Combines the autonomous agent capabilities with the internal knowledge retrieval of RAG. The agent can now strategically decide when to consult internal documentation.
    * **Task Example:** "How to install OpenShift?"
    * **Agent Capability:** Leverages RAG as a tool to answer user queries based on internal documents, intelligently determining when this knowledge source is relevant.

5.  **`Level5_agentic_and_mcp.ipynb`:**
    * **Focus:** Integrates the agent with our OpenShift, and slack environment via MCP tools, enabling real-time interaction and automation of operational tasks. This notebook explores various levels of OpenShift interaction.
    * **Task Example:** "Check the status of my OpenShift cluster. If it’s running, create a new pod named `test-pod` in the `dev` namespace." / "Review OpenShift logs for pod `slack-test`. Categorize each as ‘Normal’ or ‘Error’. If any show ‘Error’, send a Slack message to the ops team. Otherwise, show a simple summary."
    * **Agent Capability:** Utilizes `Openshift` and `slack` tools to demonstrate a complex workflow, of interacting with OCP and updating team via slack.


6.  **`Level6_agentic_MCP_and_RAG.ipynb`:**
    * **Focus:** Represents the culmination of our efforts, showcasing a complete incident response flow by integrating prompt chaining, RAG for solution retrieval, and MCP for OpenShift interaction and Slack communication.
    * **Task Example:**
        "View the logs for pod slack-test in the llama-serve OpenShift namespace. Categorize it as normal or error.",
        "search for solutions on this error and provide a summary of the steps to take .",
        "Summarize the results with the pod name, category along with a briefly explaination as to why you categorized it as normal or error and brief on the next steps to take.",
        "Send a message with the summarization to the demos channel on Slack."
    * **Agent Capability:** Combines the use of MCP tools and RAG to automate the process of analyzing pod logs, finding relevant solutions, and sending a notification to team via Slack on errors with steps to take.

By exploring these notebooks in sequence, you can gain a comprehensive understanding of the agent's development journey and its capabilities in streamlining OpenShift operations and incident management.

## Demo Recordings

- **MCP Multi-Tool Call Demo** - Watch this recorded demo showcasing the multi-tool call capabilities of MCP tools: https://youtu.be/aaxclldaVWw. The video walks through a query from the [Level 5 Agentic MCP notebook](notebooks/Level5_agentic_and_mcp.ipynb), including step-by-step instructions for setting up a Slack app, configuring the Slack MCP server, and interacting with it in action.
