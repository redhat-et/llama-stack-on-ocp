# 👋 Welcome to the Llama Stack Demos Repository! Unleash the Power of Advance AI agent on Kubernetes & OpenShift

Ready to build cutting-edge AI applications with [Llama Stack](https://github.com/meta-llama/llama-stack) on Kubernetes or OpenShift? You've come to the right place! This repository is your launchpad, packed with practical examples and demos designed to get you started quickly, whether you're a cluster admin looking to deploy or an AI developer eager to innovate.

## ✨ What You'll Discover Here

Explore the exciting capabilities of Llama Stack through our key demos:

* **Intelligent Agents Unleashed (RAG + Agent + MCP):** Dive into building sophisticated AI agents that understand documents, reason, invoke tools, and perform tasks using [Retrieval-Augmented Generation (RAG)](https://www.ibm.com/think/topics/retrieval-augmented-generation), [Model Context Protocol (MCP)](https://github.com/modelcontextprotocol), and advanced agentic workflows. 
* **Effortless Deployment & Monitoring:** Learn how to seamlessly deploy these powerful agents on Kubernetes & OpenShift using the provided manifests and monitor their performance with our integrated observability toolkit.

## 💡 Demo Architecture
Imagine a secure Llama Stack application running on OpenShift, powered by MCP tools and a [Milvus](https://milvus.io/) vector database for intelligent RAG and agentic workflows. This architecture showcases the seamless integration of these powerful components.

![Architecture Diagram](./images/architecture-diagram.jpg)

## 🛠️ Get Started: Dive into Llama Stack Demos

This repository offers tailored resources to kickstart your journey with Llama Stack:

### For Cluster Administrators (Kubernetes & OpenShift Deployment)

1.  **Understand the Demo Logic:** If you want to dive deeper into the underlying logic of this demo, head over to the [demos/rag_agentic/README.md](./demos/rag_agentic/README.md) for a comprehensive explanation.
2.  **Direct Deployment:** If you already understand the demo's logic, proceed directly to the **[kubernetes/](./kubernetes/)** folder. It's packed with the documentation and all the necessary manifests to get Llama Stack and its key components running smoothly on OpenShift or Kubernetes. This includes everything from Llama Stack itself, to efficient [vLLM](https://docs.vllm.ai/en/stable/index.html) model servers, versatile MCP servers, essential observability tools for monitoring, and even simple frontend apps so users can start interacting with the AI demos right away.

### For AI Innovators (Builders of Intelligent Applications)

1.  **Your Starting Point: The RAG/Agentic Demo Guide:** Begin your journey with the comprehensive [RAG/Agentic README](./demos/rag_agentic/README.md). This guide will introduce you to the core concepts and then naturally lead you to the progressive **notebooks** for hands-on learning, frontend documentation and some source code.
2.  **Explore Collaborative AI (Beta):** Delve deeper into agent-to-agent communication by exploring the [A2A implementation](./demos/a2a_llama_stack/) after you've grasped the basics in the RAG/Agentic demo.
3.  **Understand Evaluation:** Check out the [tests/](./tests/) directory in the main repository to learn about our evaluation methodologies for LLM and MCP tool combinations, giving you insights into building high-quality AI solutions.

## ⚙️ Ready to Deploy? Here's What You'll Need

To run these demos in their full glory, ensure your environment meets the following:

* OpenShift Cluster 4.17+
* 2 GPUs with a minimum of 40GB VRAM each.

### 🚀 Deployment Instructions

Ready to launch? Follow these simple steps to deploy the core components, including those required for the "ultimate agent" demo:

1.  Create a dedicated OpenShift project:
    ```bash
    oc new-project llama-serve
    ```
2.  Apply the Kubernetes manifests:
    ```bash
    oc apply -k kubernetes/kustomize/overlay/all-models
    ```
    This will deploy the foundational Llama Stack services, vLLM model servers, and MCP tool servers, enabling the "ultimate agent" demo.


### 🐍 Setting Up Your Development Environment

We use `uv` for managing Python dependencies, ensuring a consistent and efficient development experience. Here's how to get your environment ready:

1.  Install `uv`:
    ```bash
    pip install uv
    ```
2.  Synchronize your environment:
    ```bash
    uv sync
    ```
3.  Activate the virtual environment:
    ```bash
    source .venv/bin/activate
    ```

Now you're all set to run any Python scripts or Jupyter notebooks within the `demos/rag_agentic` directory!

---

We're excited to see what you build with Llama Stack! If you have any questions or feedback, please don't hesitate to open an issue. Happy building! 🎉
