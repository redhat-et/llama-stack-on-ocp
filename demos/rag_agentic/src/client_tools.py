from llama_stack_client.lib.agents.client_tool import client_tool

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
