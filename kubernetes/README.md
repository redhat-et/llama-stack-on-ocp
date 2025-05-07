# Kubernetes Manifests

This directory contains Kubernetes and OpenShift manifests to deploy different components of a Llama Stack ecosystem. Each subdirectory is a self-contained module with its own configuration files and deployment instructions.

## Components

- [llama-serve](./llama-serve/) - Contains the manifests for deploying different LLM models via vLLM
- [llama-stack](./llama-stack/) - Contains the manifests for deploying the Llama Stack server
- [mcp-servers](./mcp-servers/) - Contains the manifests for deploying different MCP servers for integrating with tools like Slack, GitHub, databases, and more
- [observability](./observability/) - Contains the manifests for configuring an observability stack to visualize Llama Stack telemetry and vLLM metrics
- [safety-model](./safety-model/) - Contains the manifests for deploying an auxiliary safety model using vLLM to provide moderation and filtering capabilities in Llama Stack
- [streamlit-client](./streamlit-client/) - Contains the manifests for deploying a Streamlit UI application to interact with Llama Stack

## Getting Started

Each directory includes detailed deployment and configuration instructions. Navigate into the desired folder to begin setting up that component.

## Additional Resources

- [Llama Stack](https://github.com/meta-llama/llama-stack)
- [vLLM](https://docs.vllm.ai/en/latest/)
- [Streamlit](https://streamlit.io/)
