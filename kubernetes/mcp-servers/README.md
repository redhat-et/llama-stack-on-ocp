# MCP Servers

This directory contains Kubernetes manifests and configuration files for deploying different [MCP servers](https://github.com/modelcontextprotocol/servers) in an OpenShift environment.

MCP is an open protocol that standardizes how applications provide context to LLMs. It provides a standardized way to connect AI models to different data sources and tools. MCP servers enable Large Language Models (LLMs) to interact with external systems like Slack, GitHub, databases, and more, enhancing their capabilities in real-world applications.

## Contents

- [ansible-mcp](./ansible-mcp/) - An MCP server that integrates with the Ansible platform
- [custom-mcp](./custom-mcp/) - A custom MCP server with custom tools
- [github-mcp](./github-mcp/) - GitHub MCP server for enabling file operations, repository management, search functionality, and more
- [llamastack](./llamastack/) - MCP server for managing a Llama Stack server
- [openshift-mcp](./openshift-mcp/) - Kubernetes MCP server that can perform operations on a Kubernetes or OpenShift resource such as pods, namespace, projects etc
- [slack-mcp](./slack-mcp/) - Slack MCP server that integrates with Slack, allowing LLMs to send and receive messages, manage channels, and perform other Slack-related operations.

## Getting Started

To get started, go to the directory of the MCP server you'd like to deploy, where you'll find a detailed guide with deployment instructions.
