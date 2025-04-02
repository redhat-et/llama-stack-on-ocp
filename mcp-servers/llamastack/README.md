## Commands to run
### Install required dependencies
pip install -r requirements.txt

### Run the MCP OpenAPI tool server with your remote OpenAPI spec
python mcp_server.py http://localhost:5001/openapi.json --transport sse


# Pre-Requisites

You will need the following installed on your local machine:

- `podman`
- `oc`

## Step 1: Building the Containerfile

You will need to first build a container image using the `Containerfile` and can do this by using `podman`. To build the container image from `mcp-servers/llamastack`:

```
podman build -t mcp-llamastack-server:latest -f Containerfile .
```

If running on a Mac:

```
podman build -t mcp-llamastack-server:latest --platform="linux/amd64" -f Containerfile .
```

If run successfully, you should see your image `localhost/mcp-llamastack-server` listed when you run:

```
podman images
```

## Step 2: Pushing the container image to Quay

Next, you will need to push your container image to a public image repository like [quay.io](https://quay.io/). Make sure you create an account on quay.io, if you don't have one already. Once you have an account, you will need to login:

podman login -u=<user_name> -p=<pass_word> quay.io

Once you're logged in successfully, you can now push your image by first tagging your local image:

podman tag localhost/mcp-llamastack-server:latest quay.io/<username>/mcp-llamastack-server:latest


Then you can push to your quay registry:

podman push quay.io/<username>/mcp-llamastack-server:latest


### Step 3: Deploying on OpenShift

To deploy the llamastack MCP server on OpenShift, make sure you have access to an active OpenShift cluster and namespace. You should then login to it:


oc login --token=<your user token> --server=<your openshift cluster server>


Select a suitable namespace within the cluter:

oc project <your namespace>


Deploy the llamastack MCP server application:


oc apply -f deployment.yaml


You should now see a pod running successfully in OpenShift as well as a service created for it!