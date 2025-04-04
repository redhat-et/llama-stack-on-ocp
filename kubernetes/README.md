# vLLM serve

This serves as a starting point to deploy `meta-llama/Llama-3.1-8B-Instruct` via vLLM. Long term this should be handled by RHOAI.

## Requirements

A secret must be created to allow for the vLLM server to pull in the model at startup time.

```
oc create secret generic huggingface-secret --from-literal=HF_TOKEN=hf_values
```

## Deploy

You can find the deployment file [here](https://github.com/redhat-et/agent-frameworks/tree/main/prototype/frameworks/llamastack/kubernetes/llama-serve).
The vLLM deployment will take the secret from above and use it to pull in the model. To launch the vLLM deployment run the following:

```
oc create -f llama-serve/vllm.yaml
oc expose deployment/vllm
```

## Using the vLLM server

The vLLM instance is running with a service, this service can be accessed by other namespaces in the cluster as well as outside the cluster by using port-forward.

To use port-forward run the following:

```
kubectl port-forward service/vllm 8000:8000
```

## Testing

To check if the model is running correctly, you can try the following `curl` command:

```
 curl http://localhost:8000/v1/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "meta-llama/Llama-3.1-8B-Instruct",
        "prompt": "San Francisco is a",
        "max_tokens": 200,
        "temperature": 0
    }'
```
# Guardrails

To serve Llama Guard deploy the items within the safety-model directory.

```
oc apply -f safety-model
```

# Llamastack

To run llamastack on OpenShift, we can utlize the kubernetes svc address along with providing a configmap for the unique values we want to test.


## Building Llamastack

If you need to use a specific branch or even the main branch of the upstream Llamastack repository in your container image, you can run the following steps:

```
git clone git@github.com:meta-llama/llama-stack.git
cd llama-stack

# Create the venv to install llamastack locally
python -m venv venv
source venv/bin/activate
pip install -U .

export CONTAINER_BINARY = podman
USE_COPY_NOT_MOUNT=true LLAMA_STACK_DIR=. llama stack build --template remote-vllm --image-type container

# tag the local container image and push to quay
podman tag localhost/distribution-remote-vllm:dev quay.io/redhat-et/llama:2-27-2025
podman push quay.io/redhat-et/llama:2-27-2025
```

## Building Llamastack with Milvus (in-line)

If you need to build Llamastack to use Milvus as the default in-line vector db provider in your container image, you can run the following steps:

```
git clone git@github.com:meta-llama/llama-stack.git
cd llama-stack

# Create the venv to install llamastack locally
python -m venv venv
source venv/bin/activate
pip install -U .
```

Edit the `build.yaml` in the `llama_stack/template/remote-vllm/build.yaml` to update the `vector_io` provider field and `image_type` field as shown below:

```
  providers:
    vector_io:
    - inline::milvus
image_type: container
```

Now, we can build the container.

```
export CONTAINER_BINARY = podman
USE_COPY_NOT_MOUNT=true LLAMA_STACK_DIR=. llama stack build --config llama_stack/templates/remote-vllm/build.yaml --image-type container --image-name remote-vllm-milvus
```

Once the image is built successfully you can push it to quay:

```
podman tag localhost/remote-vllm-milvus:<version tag> quay.io/<quay user name or org name>/<image name>
podman push quay.io/<quay user name or org/<image name>
```

Update the [`deployment.yaml`](https://github.com/redhat-et/agent-frameworks/blob/main/prototype/frameworks/llamastack/kubernetes/llama-stack/deployment.yaml#L28) file using the image generated above.

## Configmap

A predefined [`configmap`](https://github.com/redhat-et/agent-frameworks/blob/main/prototype/frameworks/llamastack/kubernetes/llama-stack/configmap.yaml) exists with entirely too many options, but is a placeholder for what can be added. Create the configmap defining your unique settings. Then create the CM. The [`template.yaml`](https://github.com/redhat-et/agent-frameworks/blob/main/prototype/frameworks/llamastack/kubernetes/llama-stack/template.yaml) file does not need to be modified. It contains the jinja chat template.

```
oc create -f llama-stack/configmap.yaml
oc create -f llama-stack/template.yaml
```


## Deployment

The deployment doesn't really have any unique values at this time. We will most likely learn more as we progress

```
oc create -f llama-stack/deployment.yaml
```

## Access

This deployment isn't exposed so depending on where you need to access it from outside the cluster, expose it accordingly.

If you want to deploy a chat server that points to the llamastack deployment then run the following:

```
oc expose deployment/llamastack-deployment
```

If you want to access the llama-stack externally from the cluster then you must expose the svc which will create a route:

```
oc expose svc/llamastack-deployment
```

The above will generate a route similar to this:

```
llamastack-deployment-llama-serve.apps.ocp-beta-test.nerc.mghpcc.org
```
(_**NOTE:**_ This will be unique to your environment)

## Using the endpoints

Now that everything is available in the OpenShift cluster, you can utilize the vLLM instance and the Llamastack server by ensuring that you set the following before running your tests/experiments:

```
export INFERENCE_MODEL="meta-llama/Llama-3.2-1B-Instruct"
export LLAMA_STACK_PORT=80
export INFERENCE_ADDR=vllm-llama-serve.apps.ocp-beta-test.nerc.mghpcc.org
```

(_**NOTE:**_ The INFERENCE_ADDR will be based on your OpenShift environment.)

## Testing the endpoints

To test the Llamstack server, you can run any of the examples from [here](https://github.com/redhat-et/agent-frameworks/tree/main/prototype/frameworks/llamastack/scripts). Make sure to set the following env vars before executing the scripts:

```
LLAMA_STACK_PORT=80
INFERENCE_MODEL="meta-llama/Llama-3.2-1B-Instruct"
```

You will also need to update the script with the correct connection settings for the deployed Llamstack server URL. For example, if you wish to run the [`custom-tool.py`](https://github.com/redhat-et/agent-frameworks/blob/main/prototype/frameworks/llamastack/scripts/custom-tool.py) script, you will need to update [this line](https://github.com/redhat-et/agent-frameworks/blob/main/prototype/frameworks/llamastack/scripts/custom-tool.py#L47) with the URL of your deployed Llamstack server.

(_**NOTE:**_ This will be unique to your OpenShift environment.)

```
    client = LlamaStackClient(
        base_url=f"http://<your llamastack server URL>:{os.getenv('LLAMA_STACK_PORT')}"
    )
```

You can then simply run the script like so:

```
python custom-tool.py
```

If the script runs successfully, you should see an output in the logs like so:

```
inference> The result of 25 plus 15 is 40.
DEBUG:httpcore.http11:receive_response_body.complete
DEBUG:httpcore.http11:response_closed.started
DEBUG:httpcore.http11:response_closed.complete
DEBUG:httpcore.connection:close.started
DEBUG:httpcore.connection:close.complete
```

