# Monitor Llama Stack Distributed Traces in OpenShift

Follow this README to configure an observability stack in OpenShift to visualize Llamastack telemetry.
Llamastack must be configured to collect telemetry.
This [configuration guide](./run-configuration.md) outlines how to update the deployment manifests for telemetry collection.

Before updating Llamastack to collect and visualize telemetry, deploy the observability components. Read below for how to deploy each:

* Tempo Tracing Backend
* Grafana with Tempo Datasource
* OpenTelemetryCollector Sidecar

## OpenShift Observability Operators

Operators are available from OperatorHub
The following operators must be installed in order to proceed with this example.

### Operator descriptions

1. **Red Hat Build of OpenTelemetry**: The OpenTelemetry Collector (OTC) is provided from this operator.
Metrics and traces will be distributed from the OTC to various backends. Tempo is deployed and is the tracing backend.

2. **Tempo Operator**: Provides `TempoStack` Custom Resource. This is the backend for distributed tracing.
An S3-compatible storage (Minio) is paired with Tempo.

3. **Grafana Operator**: Provides Grafana APIs including `GrafanaDashboard`, `Grafana`, and `GrafanaDataSource` that will be used to visualize telemetry.

### Tracing Backend (Tempo with Minio for S3 storage)

In order to view distributed tracing data from LLama Stack, you must deploy a tracing backend. The supported tracing backend in OpenShift
is Tempo. See the OpenShift Tempo
[documentation](https://docs.redhat.com/en/documentation/openshift_container_platform/4.18/html/distributed_tracing/distributed-tracing-platform-tempo#distr-tracing-tempo-install-tempostack-web-console_dist-tracing-tempo-installing)
for further details. Tempo must be paired with a storage solution. For this example, `MinIO` is used. The necessary resources can be created by
applying the `./tempo` manifests.

```bash
# edit storageclassName & secret as necessary
# secret and storage for testing only
oc apply --kustomize ./tempo -n llama-stack # <-update namespace to wherever Llama Stack is running
```

### OpenTelemetryCollector deployment

OpenTelemetry Collectors can be configured to aggregate telemetry from various workloads, process individual signals, and export
to various backends. This example will collect traces from Llama Stack and export as an
authenticated stream to a TempoStack in the same namespace.

#### OpenTelemetry Collector Sidecar

OpenTelemetry Collector Sidecar is created to trigger an opentelemetry-collector container with the Llama Stack deployment.
Paired with an annotation on the deployment, Llama Stack telemetry will be exported as configured.

To deploy an OpenTelemetryCollector in the `llama-stack` namespace alongside a llama stack deployment:

```bash
oc apply -f ./otel-collector/otel-collector-llamastack-sidecar.yaml
```

Any deployment with the `template.metadata.annotations` `sidecar.opentelemetry.io/inject: llamastack-otelsidecar`
will receive and export telemetry as configured in the
[otel-collector-llamstack-sidecar example](./otel-collector/otel-collector-llamastack-sidecar.yaml).

> **📝 NOTE:** If llama stack is already running, refresh the llama stack pods to trigger addition of otel-collector container in the llama-stack deployment

See [OpenTelemetryCollector Sidecar](./otel-collector/otel-collector-llamastack-sidecar.yaml) for configuration details & Tempo exporter.

### Grafana

Most users are familiar with Grafana for visualizing and analyzing telemetry. To create the Grafana resources necessary to view
Llamastack telemetry, follow the below example.

This example will deploy a Grafana instance, and Prometheus & Tempo DataSources
The prometheus datasource is the user-workload-monitoring prometheus running in `openshift-user-workload-monitoring` namespace.
This means any metrics that are collected via user-workload-monitoring in OpenShift will be visible from Grafana UI.

```bash
oc apply --kustomize ./grafana/instance
# check for grafana-sa before proceeding, since serviceaccount needs to exist before the token-secret needed for datasources
oc get sa/grafana-sa
oc apply --kustomize ./grafana/datasources
```

Upon success, you can explore Llama Stack traces from the Grafana route. To access Grafana (as configured in this repo), use
`username:password admin:admin`.


### Cluster Observability Operator Tracing UIPlugin (optional)

This section depends on Cluster Observability Operator installed in cluster. This operator is available from Operator Hub.
OpenShift provides a Tracing UI and Dashboards similar to how it provides a prometheus metrics explorer with user-workload-monitoring.
The Jaeger frontend feature of TempoStack is no longer supported by Red Hat. This has been replaced by the COO UIPlugin.
To create the `UIPlugin for Distributed Tracing`, first ensure the TempoStack described above is created. This is a prerequisite. Then, all that's necessary to view traces from
the OpenShift console at `Observe -> Traces` is to create the following [Tracing UIPlugin resource](./tracing-ui-plugin.yaml).

```bash
oc apply ./tracing-ui-plugin.yaml
```

You should now see traces and metrics in the OpenShift console, from the `Observe` tab.
