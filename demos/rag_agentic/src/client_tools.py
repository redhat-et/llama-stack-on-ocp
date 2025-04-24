from llama_stack_client.lib.agents.client_tool import client_tool
import geocoder

@client_tool
def torchtune(query: str = "torchtune"):
    """
    Answer information about torchtune.

    :param query: The query to use for querying the internet
    :returns: Information about torchtune
    """
    dummy_response = """
            torchtune is a PyTorch library for easily authoring, finetuning and experimenting with LLMs.

            torchtune provides:

            PyTorch implementations of popular LLMs from Llama, Gemma, Mistral, Phi, and Qwen model families
            Hackable training recipes for full finetuning, LoRA, QLoRA, DPO, PPO, QAT, knowledge distillation, and more
            Out-of-the-box memory efficiency, performance improvements, and scaling with the latest PyTorch APIs
            YAML configs for easily configuring training, evaluation, quantization or inference recipes
            Built-in support for many popular dataset formats and prompt templates
    """
    return dummy_response

@client_tool
def get_location(query: str = "location"):
    """
    Provide the location upon request.

    :param query: The query from user
    :returns: Information about user location
    """
    try:
        g = geocoder.ip('me')
        if g.ok:
            return f"Your current location is: {g.city}, {g.state}, {g.country}" # can be modified to return latitude and longitude if needed
        else:
            return "Unable to determine your location"
    except Exception as e:
        return f"Error getting location: {str(e)}"
