# Safety Model for Llamastack

This directory contains the deployment file for deploying a safety model i.e. `meta-llama/Llama-Guard-3-8B` via vLLM for Llamastack.

## Requirements

A secret must be created to allow for the vLLM server to pull in the model from HuggingFace at startup time.

```
oc create secret generic huggingface-secret --from-literal=HF_TOKEN=hf_values
```

## Deployment

You can find the deployment file [here](./vllm.yaml). The vLLM deployment will take the secret from above and use it to pull in the model. To launch the vLLM deployment run the following:

```
oc create -f safety-model
```

## Using the vLLM server

The vLLM instance is running with a service, this service can be accessed by other namespaces in the cluster as well as outside the cluster by using port-forward.

To use port-forward run the following:

```
oc port-forward service/vllm 8000:8000
```
