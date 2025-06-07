# Running Your Llama Stack Agent with Google A2A

Welcome! This guide provides comprehensive instructions for setting up and running a custom agent on **Llama Stack**, leveraging Google’s **Agent‑to‑Agent (A2A)** communication protocol. Follow these steps to make your agent operational.

---

## Overview

By completing this guide, you will accomplish the following:
1.  Setting up your development environment.
2.  Download the requisite code repositories.
3.  Install all necessary dependencies.
4.  Configure connection details for your Llama Stack inference server.
5.  Launch the A2A agent server(s).
6.  Execute a client application to dispatch tasks to your agent(s).

---

## Prerequisites

Before commencing, please ensure the following components are installed and accessible:
* **Python 3.11 or newer**
* **`pip`** (Python package manager)
* A **Llama Stack** inference server, running and reachable from your machine.

---

## Setup Instructions

Follow these steps to prepare your environment and the application code.

### 1. Download the Required Code

Begin by cloning two Git repositories: the Llama Stack demos and the Google A2A examples.

```bash
# Clone the Llama Stack demos repository
git clone https://github.com/opendatahub-io/llama-stack-demos.git


# Clone the Google A2A examples repository
git clone https://github.com/google-a2a/a2a-samples.git
```
*These commands will create two new directories, `llama-stack-demos` and `A2A`, in your current working folder.*

### 2. Prepare the Custom Agent Package

You will now copy the Llama Stack agent code from the `llama-stack-demos` repository into the appropriate directory within the `a2a-samples` examples structure.

```bash
# Navigate to the target directory within the A2A examples.
cd a2a-samples/samples/python/agents

# Copy the Llama Stack agent directory.
cp -r ../../../../llama-stack-demos/demos/a2a_llama_stack .
```

After the copy operation, verify that the `A2A/samples/python/agents/a2a_llama_stack/` directory has been created and contains the following files and folders:
* `__init__.py`
* `__main__.py`
* `task_manager.py`
* `A2AFleet.py`
* `A2ATool.py`
* `requirements.txt`
* `agents/`
* `cli/`
* `notebooks/`

### 3. Create and Activate a Python Virtual Environment

Employing a virtual environment is strongly recommended to manage project-specific dependencies effectively and prevent conflicts with your global Python installation or other projects.

```bash
# Navigate to the `python` directory.
cd ..

# Create a virtual environment named 'venv' using uv
uv venv
```

Next, activate the virtual environment. The activation command varies by operating system:

* **macOS / Linux:**
    ```bash
    source .venv/bin/activate
    ```
* **Windows (Command Prompt or PowerShell):**
    ```bash
    .venv\Scripts\activate
    ```
*Once activated, your terminal prompt should typically be prefixed with `(venv)`, indicating the virtual environment is active.*

### 4. Install Python Dependencies

Navigate into the `a2a_llama_stack` directory (which you just populated) and install its Python package dependencies. Ensure your virtual environment remains active.

```bash
# Navigate into the Llama Stack agent directory
cd agents/a2a_llama_stack

# Install the required packages specified in requirements.txt using uv
uv pip install -r requirements.txt
```
*You should now be located in the `a2a-samples/samples/python/agents/a2a_llama_stack` directory.*

---

## Configuration: Environment Variables

Your agent requires the network address of your Llama Stack server and the identifier of the AI model to be used. These are configured via environment variables.

| Variable          | Description                                     | Default Value               | Example Custom Value        |
|-------------------|-------------------------------------------------|-----------------------------|-----------------------------|
| `REMOTE_BASE_URL` | Address of your Llama Stack inference server.   | `http://localhost:8321`     | `http://your-llama-server` |
| `INFERENCE_MODEL_ID`        | Model identifier available on your Llama Stack. | `llama3.2:3b-instruct-fp16` | `your-custom-model-id`      |

Set these variables in the terminal session where you plan to launch the agent server (detailed in the subsequent section).

* **macOS / Linux:**
    ```bash
    export REMOTE_BASE_URL="http://localhost:8321"
    export INFERENCE_MODEL_ID="llama3.2:3b-instruct-fp16"
    ```
    *(Adjust these values if your `REMOTE_BASE_URL` or `INFERENCE_MODEL_ID` differs from the defaults.)*

* **Windows (PowerShell):**
    ```powershell
    setx REMOTE_BASE_URL "http://localhost:8321"
    setx INFERENCE_MODEL_ID "llama3.2:3b-instruct-fp16"
    ```
    *(Modify the values as necessary. Note: After using `setx`, these variables are persistently set for the current user. However, you must open a **new** PowerShell window or restart your current one for these changes to become effective in that session.)*

---

## Running the Application

You are now prepared to launch your agent. This process involves two primary stages:
1.  Launching the agent server(s).
2.  Executing a client application to send tasks to these server(s).

You can opt for a basic single-agent configuration or a more intricate multi-agent setup.

### Part 1: Launch the Agent Server(s)

The agent server is the core component that listens for and processes incoming A2A tasks.

**Important Considerations:**
* Ensure your Python virtual environment (`venv`) is **active** in the terminal session used for this step.
* Confirm that the `REMOTE_BASE_URL` and `INFERENCE_MODEL_ID` environment variables are **set** within this same terminal session.

You should currently be in the `a2a-samples/samples/python/agents/a2a_llama_stack` directory (upon completing Step 4 of the Setup Instructions). To launch the agent server module correctly, first navigate to the `a2a-samples/samples/python/` directory:

```bash
# If you are currently in a2a-samples/samples/python/agents/a2a_llama_stack:
cd ../../
# You should now be in the a2a-samples/samples/python/ directory.
```

Now, select **one** of the following server configurations:

#### Option A: Basic Setup (Single Agent Server)

This configuration runs a single agent, named `a2a_custom_tools`, which listens on port `10011`. This agent will interface with the Llama Stack for its operational tasks.

```bash
# Ensure you are in the a2a-samples/samples/python/ directory
# And your virtual environment is active.
uv run --active python -m agents.a2a_llama_stack --agent-name a2a_custom_tools --port 10011
```

#### Option B: Multi-Agent Setup (Multiple Agent Servers)

This setup illustrates a more complex scenario involving three distinct agents: a planner, a tools agent, and a composer, each operating on a separate port.

```bash
# Ensure you are in the A2A/samples/python/ directory

# Terminal 1: Launch the planner agent
uv run --active python -m agents.a2a_llama_stack --agent-name a2a_planner --port 10010

# Terminal 2: Launch the custom tools agent
# (Open a new terminal window/tab, activate venv, and set environment variables before running)
uv run --active python -m agents.a2a_llama_stack --agent-name a2a_custom_tools --port 10011

# Terminal 3: Launch the composer agent
# (Open another new terminal window/tab, activate venv, and set environment variables before running)
uv run --active python -m agents.a2a_llama_stack --agent-name a2a_composer --port 10012
```
*For the multi-agent setup (Option B), each `python -m ...` command initiates a server that will occupy its terminal. You will need to open multiple terminal windows/tabs or manage these processes in the background.*

A successful agent server launch will display a confirmation message in the console, similar to:
```
INFO | Agent listening on 0.0.0.0:XXXX
```
(Where `XXXX` corresponds to the agent's port number, e.g., `10010`, `10011`, or `10012`).

*Keep these agent server terminal(s) running while you proceed to the client setup.*

### Part 2: Send Tasks from the Client

With the agent server(s) operational, you can now use a client application to dispatch tasks. This requires opening a **new terminal window or tab**.

1.  **Setting up the Client Script Environment:**
    ```bash
    # Navigate to the client script directory:
    cd a2a-samples/samples/python
    ```

2.  **Navigate to the client script directory:**
    The client application is typically executed from the `cli` directory, located within the `a2a_llama_stack` agent's sample code.
    ```bash
    cd agents/a2a_llama_stack/cli
    ```

3.  **Run the client application:**
    The `uv run` command, followed by the specific client script (`basic_client.py` or `multi_agent_client.py`), executes the client. The arguments passed depend on your chosen server setup (Option A or B).

    #### If you used "Option A: Basic Setup" for the agent server:
    Run the `basic_client.py` script, directing it to the `a2a_custom_tools` agent:
    ```bash
    uv run --active basic_client.py --agent http://localhost:10011
    ```

    #### If you used "Option B: Multi-Agent Setup" for the agent servers:
    Run the `multi_agent_client.py` script, providing the network addresses for all three agents. It is crucial that the `a2a_planner` agent (`http://localhost:10010`) is specified first.
    ```bash
    uv run --active multi_agent_client.py --agent http://localhost:10010 --agent http://localhost:10011 --agent http://localhost:10012
    ```

Upon executing the appropriate `uv run` command, the client will attempt to establish a connection with the agent server(s) and enable task interaction.

---

### Built-in Sample Tools

The custom Llama Stack agent you have deployed includes several sample tools for demonstration:

| Tool            | Description                    |
|-----------------|--------------------------------|
| `random_number` | Returns a random integer.      |
| `get_date`      | Returns today’s date.          |

You can experiment with invoking these tools via the client interface once it is connected.

---

## 🎉 Congratulations!

Your custom Llama Stack agent should now be running successfully using the Google A2A protocol and be prepared to accept tasks from the client.

Should you encounter any difficulties, please review each step, paying particular attention to:
* Verification of prerequisites and their versions.
* Correct activation of the Python virtual environment.
* Accuracy of directory paths used in `cd`, `cp`, and script execution commands.
* Proper configuration of environment variables (`LLAMA_STACK_URL`, `MODEL_ID`).
* Alignment of client commands with the chosen server setup (Basic or Multi-Agent).
```
