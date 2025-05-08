# Llama Stack Demos

This repo contains a collection of examples and demos for both cluster admins and AI developers to help them start building [Llama Stack](https://github.com/meta-llama/llama-stack) based apps on OpenShift or Kubernetes.

**For Cluster Admins**, please take a look at the [kubernetes/](./kubernetes/) directory of this repo. It contains useful documentation along with all the manifests required to deploy each of the components of a Llama Stack based app onto OpenShift or Kubernetes. That includes Llama Stack itself, as well as [vLLM](https://docs.vllm.ai/en/stable/index.html) model servers, [MCP](https://github.com/modelcontextprotocol) tool servers, an observability toolkit, and simple frontend apps for users to interact with the AI demos.

**For AI Developers**, please take a look at the [demos/](./demos/) directory of this repo. It contains useful documentation as well as all the notebooks, Containerfiles and application code needed to learn about developing AI applications with Llama Stack and deploying them on OpenShift or Kubernetes.

Current Demos:

* [RAG/Agentic](./demos/rag_agentic/)


## Repository Structure

- [demos/](./demos/) – Contains demo notebooks and app code, focusing on RAG and agentic AI use cases.
  - [a2a_llama_stack/](./demos/a2a_llama_stack/) – Guide for running a custom agent on Llama Stack using Google’s Agent-to-Agent (A2A) protocol.
  - [rag_agentic/](./demos/rag_agentic/) – Demo integrating Retrieval Augmented Generation (RAG) with agent-based workflows.
    - [src/](./demos/rag_agentic/src/) – Server-side logic, RAG pipeline, and agent tool invocation.
    - [frontend/build](./demos/rag_agentic/frontend/build) – Build artifacts for Streamlit UI.
    - [notebooks/](./demos/rag_agentic/notebooks/) – Jupyter notebooks for hands-on experimentation.
- [distribution/](./distribution/) – Container build files for the Llama Stack distribution image.
- [images/](./images/) – Architecture diagrams and visual documentation assets.
- [kubernetes/](./kubernetes/) – Kubernetes manifests for deploying Llama Stack components.
- [tests/](./tests/) – Test scripts and evaluation tools for the demos.
- [local_setup_guide.md](./local_setup_guide.md) – Setup guide to run Llama Stack locally.
- [Makefile](./Makefile) – Automation targets for development and deployment.
- [pyproject.toml](./pyproject.toml) – Python project configuration and dependencies.
- [uv.lock](./uv.lock) – Lock file for deterministic environment setup.
- [README.md](./README.md) – You're here! The main guide and entry point for understanding the repository.


## Example Architecture
The below diagram is an example architecture for a secure Llama Stack based application deployed on OpenShift (OCP) using both MCP tools and a [Milvus](https://milvus.io/) vectorDB for its agentic and RAG based workflows. This is the same architecture that has been implemented in the [RAG/Agentic](./demos/rag_agentic/) demos.

![Architecture Diagram](./images/architecture-diagram.jpg)

## Requirements
The following scenarios requires at minimum the following:

* OpenShift Cluster 4.17+
* 2 GPUs with a minimum of 40GB VRAM each

## Deploy
A `kustomization.yaml` file exists to launch all required Kubernetes objects for the scenarios defined in the repository. To create run the following.

```
oc new-project llama-serve
oc apply -k kubernetes/kustomize/overlay/all-models
```

To execute the evaluation [notebook](./demos/rag_agentic/notebooks/Level3.5_agentic_RAG_with_reference_eval.ipynb),
we recommend the following:
* Inject the OpenAI API token into the Llama Stack application as a Secret with: `oc create secret generic openai-secret --from-literal=OPENAI_API_KEY=${OPENAI_API_KEY}`
* Use the dedicated overlay as: `oc apply -k kubernetes/kustomize/overlay/eval`

## Running Demos and Notebooks

This project uses `uv` as its package manager for the python based notebooks and demo scripts. You can quickly set up your working environment by following these steps:

1) `pip install uv`
2)  `uv sync`
3) `source .venv/bin/activate`

Once you are using the virtual environment, you should be good to run any of the scripts or notebooks in `demos/`.
