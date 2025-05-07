# Streamlit

This directory contains a [Streamlit](https://streamlit.io/) frontend application designed to interact with the Llama Stack backend. It provides a user-friendly interface to demonstrate the capabilities of Llama Stack, including chat interactions and tool integrations.

## Deploying on OpenShift

To deploy a Streamlit UI on Openshift, you can use the [deployment.yaml](./deployment.yaml) and run the following. The deployment also integrates [OAuth proxy authentication](https://github.com/opendatahub-io/llama-stack-demos/blob/main/kubernetes/streamlit-client/deployment.yaml#L17) to securely access the Streamlit application (this is optional):

```
oc create -f streamlit-client
```

In order to connect the Streamlit UI to your Llamastack server, you will need to update the deployment to specify your Llamstack server endpoint [here](https://github.com/opendatahub-io/llama-stack-demos/blob/main/kubernetes/streamlit-client/deployment.yaml#L43).

Once the deployment is created successfully, you can create a [service](service.yaml) and a [route](route.yaml) to expose the Streamlit application. You will then be able to access the Streamlit UI through the URL created.
