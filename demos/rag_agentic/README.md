# RAG/Agentic/MCP Demos

## Overview
This folder offers a practical learning path for anyone interested in understanding and gaining hands-on experience with LlamaStack and AI agents. The demos are structured progressively, starting from foundational concepts and gradually advancing to more complex implementations, helping users build the skills needed to develop AI-powered applications.

1. **Level 1**: Understand foundational RAG concepts (Low difficulty)
2. **Level 2**: Try out simple agentic demo with single tool ussage. (Medium-low difficulty)
3. **Level 3**: Combine RAG with agentic capabilities (Medium difficulty)
4. **Level 4**: Explore advanced agentic RAG features (Medium difficulty)
more to be continue.

## Folder Structure
- `notebooks/`: Jupyter notebooks for learning RAG and agent implementation
- `src/`: Python source files for production implementation
- `frontend/`: Containerfile for building the streamlit UI.

## Getting Started
### 1. `notebooks/`: Start with notebooks in order
- `Level1_foundational_RAG.ipynb`: Start here! Learn the basics of RAG
- `Level2_simple_agentic_with_websearch.ipynb`: Add web search capabilities to your agent
- `Level3_agentic_RAG.ipynb`: Combine RAG with agentic capabilities
- `Level4_agentic_and_mcp.ipynb`: Advanced topics in agentic RAG

### 2. Review source code in `src/`
Contains Python source files that implement the concepts from the notebooks. Good for future production stage.
Before running scripts, remember to set up your environment variables using `.env.example` as a template

### 3. Deploy and play with `frontend/` Streamlit UI 
This folder contains the containerfile to build a user interface based on the playground UI provided by llama-stack. The playground UI is a Streamlit application that provides an interactive interface for testing and experimenting with language models. 
For more information, visit: https://llama-stack.readthedocs.io/en/latest/playground
