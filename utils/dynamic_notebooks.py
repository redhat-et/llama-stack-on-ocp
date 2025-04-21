#!/usr/bin/env python3
import os
import yaml
import json
import sys
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Generate a ConfigMap from Jupyter notebooks.')
    parser.add_argument('--notebook-dir', default='demos/rag_agentic/notebooks',
                        help='Directory containing Jupyter notebooks')
    parser.add_argument('--output-dir', default='kubernetes/notebooks',
                        help='Directory for output YAML files')
    parser.add_argument('--configmap-name', default='rag-agentic-notebooks-configmap',
                        help='Name of the ConfigMap to generate')
    parser.add_argument('--pvc-name', default='rag-agentic-notebooks-pvc',
                        help='Name of the PVC to use in the deployment')

    return parser.parse_args()


def generate_configmap(notebook_dir, output_dir, configmap_name):
    """Generate a ConfigMap from Jupyter notebooks."""

    # Create directory for output if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "configmap-notebooks.yaml")

    # Find all notebook files
    notebook_files = []
    for filename in os.listdir(notebook_dir):
        if filename.endswith(".ipynb"):
            notebook_files.append(filename)

    if not notebook_files:
        print("No notebook files found in directory:", notebook_dir)
        sys.exit(1)

    # Initialize ConfigMap data
    data = {}

    # Read each notebook and add to data
    for filename in notebook_files:
        filepath = os.path.join(notebook_dir, filename)
        print(f"Processing notebook: {filepath}")

        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                notebook_content = file.read()

                # Validate that it's a proper JSON (notebook)
                json.loads(notebook_content)

                # Add to ConfigMap data
                data[filename] = notebook_content
        except Exception as e:
            print(f"Error processing {filepath}: {str(e)}")
            sys.exit(1)

    # Create ConfigMap
    configmap = {
        "apiVersion": "v1",
        "kind": "ConfigMap",
        "metadata": {
            "name": configmap_name
        },
        "data": data
    }

    # Create parent YAML structure
    kubernetes_obj = {
        "apiVersion": "v1",
        "kind": "List",
        "items": [configmap]
    }

    # Write to file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        yaml.dump(kubernetes_obj, outfile, default_flow_style=False)

    print(f"ConfigMap generated successfully: {output_file}")
    print(f"Included {len(notebook_files)} notebooks")

    return output_file, notebook_files


def generate_deployment(output_dir, configmap_name, pvc_name, notebook_names):
    """Generate an OpenShift AI deployment YAML."""

    output_file = os.path.join(output_dir, "openshift-ai-notebooks-deployment.yaml")

    # Create complete deployment manifest
    deployment = {
        "apiVersion": "v1",
        "kind": "List",
        "items": [
            # NotebookServer
            {
                "apiVersion": "datasciencepipelines.opendatahub.io/v1alpha1",
                "kind": "NotebookServer",
                "metadata": {
                    "name": "rag-agentic-notebooks",
                    "labels": {
                        "app": "rag-agentic-notebooks"
                    }
                },
                "spec": {
                    "replicas": 1,
                    "template": {
                        "spec": {
                            "containers": [
                                {
                                    "name": "notebook",
                                    "image": "quay.io/opendatahub/workbench-images:jupyter-datascience-ubi9-python-3.9-2023b",
                                    "workingDir": "/opt/app-root/src",
                                    "resources": {
                                        "limits": {
                                            "cpu": "2",
                                            "memory": "8Gi"
                                        },
                                        "requests": {
                                            "cpu": "1",
                                            "memory": "4Gi"
                                        }
                                    },
                                    "volumeMounts": [
                                        {
                                            "name": "notebooks-data",
                                            "mountPath": "/opt/app-root/src/notebooks"
                                        }
                                    ]
                                }
                            ],
                            "volumes": [
                                {
                                    "name": "notebooks-data",
                                    "persistentVolumeClaim": {
                                        "claimName": pvc_name
                                    }
                                }
                            ]
                        }
                    }
                }
            },
            # PVC
            {
                "apiVersion": "v1",
                "kind": "PersistentVolumeClaim",
                "metadata": {
                    "name": pvc_name
                },
                "spec": {
                    "accessModes": ["ReadWriteOnce"],
                    "resources": {
                        "requests": {
                            "storage": "10Gi"
                        }
                    }
                }
            },
            # Job to copy notebooks
            {
                "apiVersion": "batch/v1",
                "kind": "Job",
                "metadata": {
                    "name": "copy-notebooks-job",
                    "labels": {
                        "app": "copy-notebooks-job"
                    }
                },
                "spec": {
                    "template": {
                        "spec": {
                            "containers": [
                                {
                                    "name": "copy-notebooks",
                                    "image": "registry.access.redhat.com/ubi8/ubi-minimal:latest",
                                    "command": ["/bin/sh", "-c"],
                                    "args": [
                                        "mkdir -p /notebooks\n"
                                        "# Copy notebook files into the PVC\n"
                                        "cp -r /source/* /notebooks/\n"
                                        "echo \"Notebooks copied successfully\""
                                    ],
                                    "volumeMounts": [
                                        {
                                            "name": "source-volume",
                                            "mountPath": "/source"
                                        },
                                        {
                                            "name": "notebooks-data",
                                            "mountPath": "/notebooks"
                                        }
                                    ]
                                }
                            ],
                            "volumes": [
                                {
                                    "name": "source-volume",
                                    "configMap": {
                                        "name": configmap_name
                                    }
                                },
                                {
                                    "name": "notebooks-data",
                                    "persistentVolumeClaim": {
                                        "claimName": pvc_name
                                    }
                                }
                            ],
                            "restartPolicy": "Never"
                        }
                    },
                    "backoffLimit": 2
                }
            }
        ]
    }

    # Write the deployment file
    with open(output_file, 'w') as outfile:
        yaml.dump(deployment, outfile, default_flow_style=False)

    print(f"Deployment YAML generated successfully: {output_file}")
    print(f"Included notebooks: {', '.join(notebook_names)}")

    return output_file


def main():
    args = parse_args()

    # Generate ConfigMap
    configmap_file, notebook_names = generate_configmap(
        args.notebook_dir, args.output_dir, args.configmap_name
    )

    # Generate deployment YAML
    deployment_file = generate_deployment(
        args.output_dir, args.configmap_name, args.pvc_name, notebook_names
    )

if __name__ == "__main__":
    main()
