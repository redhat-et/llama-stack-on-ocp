from ...task_manager import AgentTaskManager, SUPPORTED_CONTENT_TYPES

AGENT_CONFIG = {
    "agent_params": {
        "model_env_var": "INFERENCE_MODEL_ID",
        "default_model": "llama3.1:8b-instruct-fp16",
        "instructions": "You are an orchestration assistant. Ensure you count correctly the number of skills needed.",
        "max_infer_iters": 10,
        "sampling_params": {
            "strategy": {"type": "greedy"},
            "max_tokens": 4096,
        },
        "tools": []
    },

    "task_manager_class": AgentTaskManager,
    "agent_card_params": {
        "name": "Orchestration Agent",
        "description": "Plans which tool to call for each user question",
        "version": "0.1.0",
        "default_input_modes": ["text/plain"],
        "default_output_modes": SUPPORTED_CONTENT_TYPES,
        "capabilities_params": {
            "streaming": False,
            "pushNotifications": False,
            "stateTransitionHistory": False,
        },
        "skills_params": [
            {
                "id": "orchestrate",
                "name": "Orchestration Planner",
                "description": "Plan user questions into JSON steps of {skill_id}",
                "tags": ["orchestration"],
                "examples": ["Plan: What's today's date and a random number?"],
                "inputModes": ["text/plain"],
                "outputModes": ["application/json"],
            }
        ]
    },
    "default_port": 10010,
}
