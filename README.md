# Llama Stack Demos

This repo contains a collection of examples and demos for both cluster admins and AI developers to help them start building [Llama Stack](https://github.com/meta-llama/llama-stack) based apps on OpenShift or Kubernetes.

**For Cluster Admins**, please take a look at the [kubernetes/](./kubernetes/) directory of this repo. It contains useful documentation along with all the manifests required to deploy each of the components of a Llama Stack based app onto OpenShift or Kubernetes. That includes Llama Stack itself, as well as [vLLM](https://docs.vllm.ai/en/stable/index.html) model servers, [MCP](https://github.com/modelcontextprotocol) tool servers, an observability toolkit, and simple frontend apps for users to interact with the AI demos.

**For AI Developers**, please take a look at the [demos/](./demos/) directory of this repo. It contains useful documentation as well as all the notebooks, Containerfiles and application code needed to learn about developing AI applications with Llama Stack and deploying them on OpenShift or Kubernetes.

Current Demos:

* [RAG/Agentic](./demos/rag_agentic/)





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

## Getting Started

1. **Learn the Basics**: Start with [RAG/Agentic README](./demos/rag_agentic/README.md) to understand core concepts.
2. **Hands-on Learning**: Follow the progressive notebooks in [notebooks](./demos/rag_agentic/notebooks/) from Level 1 simple RAG to advanced agent implementations.
3. **UI Development**: Build and run the [Streamlit playground](./demos/rag_agentic/frontend/) to interact with agents and explore tool calling.
4. **A2A with LlamaStack**: Study [A2A implementation](./demos/a2a_llama_stack/) for agent-to-agent communication (Beta stage).
5. **Deployment**: Review [kubernetes](./kubernetes/) for OpenShift/Kubernetes deployment.
6. **Testing**: Check [tests](./tests/) for evaluation methodologies and performance analysis of LLM and MCP tool combinations.
