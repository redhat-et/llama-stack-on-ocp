# Integrating a Custom Agent with Google A2A on **Llama Stack**

This guide walks you through running a custom agent on **Llama Stack** using Google’s **Agent‑to‑Agent (A2A)** protocol.

---

## 🛠 Prerequisites

- **Python 3.8 or newer**
- **`pip`** (Python package manager)
- A **Llama Stack** inference server running and reachable

---

## 1 — Download the Code

```bash
# Clone the Llama Stack demos
git clone https://github.com/opendatahub-io/llama-stack-demos.git

# Clone the Google A2A examples
git clone https://github.com/google/A2A.git
```

---

## 2 — Create & Activate a Virtual Environment

```bash
python3 -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows
venv\Scripts\activate
```

---

## 3 — Prepare the Agent Package

```bash
# Move the Llama Stack agent into the A2A samples
cd A2A/samples/python/agents
cp -r ../../../../llama-stack-demos/demos/a2a_llama_stack .
```

Verify that **`a2a_llama_stack/`** now contains:

- `__init__.py`
- `__main__.py`
- `task_manager.py`
- `agent.py`

---

## 4 — Install Python Dependencies

```bash
cd a2a_llama_stack
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## 5 — Set Environment Variables

| Variable          | Description                         | Default                   |
|-------------------|-------------------------------------|---------------------------|
| `LLAMA_STACK_URL` | Llama Stack server address          | `http://localhost:8321`   |
| `MODEL_ID`        | Model identifier on Llama Stack     | `llama3.2:3b-instruct-fp16` |

**macOS / Linux**

```bash
export LLAMA_STACK_URL=http://localhost:8321
export MODEL_ID=llama3.2:3b-instruct-fp16
```

**Windows (PowerShell)**

```powershell
setx LLAMA_STACK_URL "http://localhost:8321"
setx MODEL_ID "llama3.2:3b-instruct-fp16"
```

---

## 6 — Launch the Agent

```bash
# From A2A/samples/python
cd ../..
python -m agents.a2a_llama_stack --port 10010
```

A successful start prints something like:

```
INFO | Agent listening on 0.0.0.0:10010
```

---

## 7 — Send Tasks from the CLI Host

Open a **new terminal** and run:

```bash
source venv/bin/activate
cd A2A/samples/python/hosts/cli
uv run . --agent http://localhost:10010
```

### Built‑in sample tools

| Tool            | Description                    |
|-----------------|--------------------------------|
| `random_number` | Returns a random integer       |
| `get_date`      | Returns today’s date           |

---

### 🎉 Done!

Your custom agent is now running and ready to accept A2A tasks.
