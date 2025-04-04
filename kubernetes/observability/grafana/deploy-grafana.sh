#!/bin/sh

# This will fail if the GrafanaOperator is not installed 
# TODO: replace this with kustomize script & add the clusterrole & rolebinding yamls

MONITORING_NS=observability-hub
SECRET=grafana-sa-token

oc apply -f $(pwd)/instance-with-prom-tempo-ds/02-grafana-serviceaccount.yaml -n $MONITORING_NS
oc apply -f $(pwd)/instance-with-prom-tempo-ds/02-grafana-sa-token-secret.yaml -n $MONITORING_NS
oc apply -f $(pwd)/instance-with-prom-tempo-ds/02-grafana-instance.yaml -n $MONITORING_NS
oc apply -f $(pwd)/instance-with-prom-tempo-ds/03-grafana-route.yaml -n $MONITORING_NS
oc adm policy add-cluster-role-to-user cluster-monitoring-view -z grafana-sa
oc adm policy add-cluster-role-to-user openshift-cluster-monitoring-view -z grafana-sa
oc adm policy add-cluster-role-to-user tempostack-traces-reader -z grafana-sa
oc adm policy add-role-to-user edit -z grafana-sa -n $MONITORING_NS
oc apply -f instance-with-prom-tempo-ds/04-grafana-datasources.yaml -n $MONITORING_NS

