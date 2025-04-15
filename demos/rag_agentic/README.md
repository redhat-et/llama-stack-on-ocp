# RAG/Agentic/MCP Demos

## Overview
This folder offers a practical learning path for anyone interested in understanding and gaining hands-on experience with LlamaStack and AI agents. The demos are structured progressively, starting from foundational concepts and gradually advancing to more complex implementations, helping users build the skills needed to develop AI-powered applications.

1. **Level 1**: Understand foundational RAG concepts (Low difficulty)
2. **Level 2**: Try out simple agentic demo with single tool ussage. (Medium-low difficulty)
3. **Level 3**: Combine RAG with agentic capabilities (Medium difficulty)
4. **Level 4**: Explore advanced agentic + MCP (model context protocol) examples (Medium difficulty)


## Folder Structure
- [`notebooks/`](notebooks/): Jupyter notebooks for learning RAG and agent implementation
- [`src/`](src/): Python source files for production implementation
- [`frontend/`](frontend/): Containerfile for building the streamlit UI.

## Getting Started
### 1. [`notebooks/`](notebooks/): Start with notebooks in order
- [Level1_foundational_RAG.ipynb](notebooks/Level1_foundational_RAG.ipynb): Start here! Learn the basics of RAG.
- [Level2_simple_agentic_with_websearch.ipynb](notebooks/Level2_simple_agentic_with_websearch.ipynb): Add web search capabilities to your agent.
- [Level3_agentic_RAG.ipynb](notebooks/Level3_agentic_RAG.ipynb): Agentic RAG example, combining RAG with agentic capabilities.
- [Level4_agentic_and_mcp.ipynb](notebooks/Level4_agentic_and_mcp.ipynb): Advanced topics in agentic and MCP, showcasing  sequential tool calls and conditional logic within an agentic workflow.

### 2. Review source code in [`src/`](src/)
Contains Python source files that implement the concepts from the notebooks. Good for future production stage.
Before running scripts, remember to set up your environment variables using [.env.example](src/.env.example) as a template

### 3. Deploy and play with [`frontend/`](frontend/) Streamlit UI
This folder contains the containerfile to build a user interface based on the playground UI provided by llama-stack. The playground UI is a Streamlit application that provides an interactive interface for testing and experimenting with language models.
For more information, visit: https://llama-stack.readthedocs.io/en/latest/playground
