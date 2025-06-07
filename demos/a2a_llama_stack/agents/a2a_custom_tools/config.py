from ...task_manager import AgentTaskManager, SUPPORTED_CONTENT_TYPES
from .tools import random_number_tool, date_tool # Import tools

AGENT_CONFIG = {
    "agent_params": {
        "model_env_var": "INFERENCE_MODEL_ID",
        "default_model": "llama3.1:8b-instruct-fp16",
        "instructions": (
            "You have access to two tools:\n"
            "- random_number_tool: generates one random integer between 1 and 100\n"
            "- date_tool: returns today's date in YYYY-MM-DD format\n"
            "Always use the appropriate tool to answer user queries."
        ),
        "tools": [random_number_tool, date_tool],
        "max_infer_iters": 3,
        "sampling_params": {
            "strategy": {"type": "greedy"},
            "max_tokens": 4096,
        },
    },

    "task_manager_class": AgentTaskManager,
    "agent_card_params": {
        "name": "Custom Agent",
        "description": "Generates random numbers or retrieve today's dates",
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
                "id": "random_number_tool",
                "name": "Random Number Generator",
                "description": "Generates a random number between 1 and 100",
                "tags": ["random"],
                "examples": ["Give me a random number between 1 and 100"],
                "inputModes": ["text/plain"],
                "outputModes": ["text/plain"],
            },
            {
                "id": "date_tool",
                "name": "Date Provider",
                "description": "Returns today's date in YYYY-MM-DD format",
                "tags": ["date"],
                "examples": ["What's the date today?"],
                "inputModes": ["text/plain"],
                "outputModes": ["text/plain"],
            }
        ]
    },
    "default_port": 10011,
}
