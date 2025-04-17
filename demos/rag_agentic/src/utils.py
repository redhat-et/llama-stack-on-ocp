import json
from rich.pretty import pprint
from termcolor import cprint

def step_printer(steps):
    """
    Print the steps of an agent's response in a formatted way.
    Note: stream need to be set to False to use this function.
    Args:
    steps: List of steps from an agent's response.
    """
    for i, step in enumerate(steps):
        step_type = type(step).__name__
        print("\n"+"-" * 10, f"📍 Step {i+1}: {step_type}","-" * 10)
        if step_type == "ToolExecutionStep":
            print("🔧 Executing tool...")
            pprint(json.loads(step.tool_responses[0].content))
        else:
            if step.api_model_response.content:
                print("🤖 Model Response:")
                cprint(f"{step.api_model_response.content}\n", "yellow")
            elif step.api_model_response.tool_calls:
                tool_call = step.api_model_response.tool_calls[0]
                print("🛠️ Tool call Generated:")
                cprint(f"Tool call: {tool_call.tool_name}, Arguments: {json.loads(tool_call.arguments_json)}", "yellow")
    print("="*10, "Query processing completed","="*10,"\n")
