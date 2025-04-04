# Llama Stack on OCP

## Requirements
The following scenario requires at minimum the following:

* OpenShift Cluster 4.17+
* 8 GPUs free (A100 or H100)

## Deploy
A `kustomization.yaml` file exists to launch all required Kubernetes objects for the scenarios defined in the repository. To create run the following.

```
oc create project llama-serve
oc apply -k kubernetes
```
