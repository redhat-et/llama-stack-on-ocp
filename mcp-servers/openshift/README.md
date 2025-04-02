# Steps for deploying the OpenShift MCP server on OpenShift

The [OpenShift MCP server](https://github.com/manusa/kubernetes-mcp-server) is a Kubernetes MCP server implementation configured with a few tools that can:

- Automatically view and manage the current Kubernetes `.kube/config` or in-cluster configuration
- Use tools to perform operations on any Kubernetes or OpenShift resource such as:
    - **Pod operations** - It can list, get, delete, show logs, exec, run pods
    - **Namespace operations** - It can list Kubernetes Namespaces
    - **Events** - View Kubernetes events in all namespaces or in a specific namespace
    - **Projects** - List OpenShift Projects

## Pre-Requisites

You will need the following installed on your local machine:

- `podman`
- `oc`

## Step 1: Building the Containerfile

You will need to first build a container image using the `Containerfile` and can do this by using `podman`. To build the container image from the current directory:

```
podman build -t ocp-mcp-server:latest -f Containerfile .
```

If running on a Mac:

```
podman build -t ocp-mcp-server:latest --platform="linux/amd64" -f Containerfile .
```

If run successfully, you should see your image `localhost/ocp-mcp-server` listed when you run:

```
podman images
```

## Step 2: Pushing the container image to Quay

Next, you will need to push your container image to a public image repository like [quay.io](https://quay.io/). Make sure you create an account on quay.io, if you don't have one already. Once you have an account, you will need to login:

```
podman login -u=<user_name> -p=<pass_word> quay.io
```

Once you're logged in successfully, you can now push your image by first tagging your local image:

```
podman tag localhost/ocp-mcp-server:latest quay.io/<username>/ocp-mcp-server:latest
```

Then you can push to your quay registry:

```
podman push quay.io/<username>/ocp-mcp-server:latest
```

### Step 3: Deploying on OpenShift

To deploy the OpenShift MCP server on OpenShift, make sure you have access to an active OpenShift cluster and namespace. Note that as this MCP server is implemented to perform certain operations on a OpenShift/Kubernetes environment you will need to setup a `ServiceAccount` with `edit` RoleBinding access to allow suitable permissions for the MCP server to execute those operations. This has been defined in the `deployment.yaml`.

**Login to Openshift**

```
oc login --token=<your user token> --server=<your openshift cluster server>
```

Select a suitable namespace within the cluter:

```
oc project <your namespace>
```

**Deploy the OpenShift MCP server application**:

```
oc apply -f ../../kubernetes/mcp-servers/openshift-mcp/openshift-deployment.yaml
```

You should now see a pod running successfully in OpenShift as well as a service created for it! You should see an address created for the service in your OpenShift something like `http://172.xx.yyy.zzz:8000`.

### Step 4: Testing the OpenShift MCP server

You can run the example sript in `app/src/0_simple_agent.py` by modifying the following:

- Set the `REMOTE_MCP_URL` env var to `http://<your mcp service endpoint>:8000/sse`
- Set the `REMOTE_BASE_URL` env var to your hosted llama stack server
- Provide a suitable user query to test. You can try an example user prompt like "Please list all the pods running in my xyz namespace?" and pass it [here](https://github.com/redhat-et/llama-stack-on-ocp/blob/main/app/src/0_simple_agent.py#L74)

Then run the script like:

```
python 0_simple_agent.py -r -a
```