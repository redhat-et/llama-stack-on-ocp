# Kustomize Overlay: Model as a Service (MaaS)

## Overview

This overlay is designed to support allow for the deployment of this demo using MaaS

## Setup Instructions

### Step 1: Configure Secrets

1. Locate the `maas-example-secret.yaml` file.
1. Rename the file to `maas-private-secret.yaml`:

    ```sh
    mv maas-example-secret.yaml maas-private-secret.yaml
    ```

1. Edit the `maas-private-secret.yaml` file to include model information

> [!NOTE]
> We have added `maas-private-secret.yaml` to try to prevent accidental exposure.

> [!TIP]
> If preferred secret can also be created manually
