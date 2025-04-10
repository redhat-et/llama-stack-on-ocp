# Llama Stack Demos
## Overview
This document provides an overview of the architecture and deployment process for the Llama Stack on OpenShift (OCP). It demonstrates how the Llama Stack agentic framework, vLLM agents, and multiple MCP servers are interconnected and deployed within an OpenShift cluster. The architecture diagram below illustrates the logical flow and integration of these components.

![Architecture Diagram](./images/architecture-diagram.jpg)

## Requirements
The following scenario requires at minimum the following:

* OpenShift Cluster 4.17+
* 8 GPUs free (A100 or H100)

## Deploy
A `kustomization.yaml` file exists to launch all required Kubernetes objects for the scenarios defined in the repository. To create run the following.

```
oc new-project llama-serve
oc apply -k kubernetes
```
## Running Demos and Notebooks

This project uses `uv` as its package manager for the python based notebooks and demo scripts. You can quickly set up your working environment by following these steps:

1) `pip install uv`
2)  `uv sync`
3) `source .venv/bin/activate`

Once you are using the virtual environment, you should be good to run any of the scripts or notebooks in `demos/`.  

