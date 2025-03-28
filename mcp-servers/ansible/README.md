# Ansible MCP Server

Quick guide to build and deploy an Ansible MCP server on OpenShift Container Platform (OCP).

---

##  Prerequisites

- [Podman](https://podman.io) installed
- Access to [Quay.io](https://quay.io) with push permissions
- Access to an OpenShift cluster and `oc` CLI
- AAP token and URL credentials

---

##  Build and Push with Podman

```bash
# Build for amd64 (required for OpenShift)
podman build --arch amd64 --os linux -t quay.io/<your-username>/ansible-mcp:amd-0.1.0 -f Containerfile .

# Push to Quay
podman push quay.io/<your-username>/ansible-mcp:amd-0.1.0
```

## Deploy on OpenShift

Make sure you're logged in to your OpenShift namespace.

```bash
# Apply AAP credentials secret
oc apply -f aap-secret.yaml -n <namespace>

# Apply deployment
oc apply -f deployment.yaml -n <namespace>
```

