#!/bin/bash

echo "📊 Dhātu Processing Cluster Status"
echo "================================="

# Kubernetes cluster status
echo "☸️ Kubernetes Status:"
kubectl get nodes
kubectl get pods -n dhatu-processing

# Resource usage
echo "💾 Resource Usage:"
kubectl top nodes
kubectl top pods -n dhatu-processing

# Performance metrics
echo "⚡ Performance Metrics:"
kubectl exec -n dhatu-processing deployment/dhatu-cpu-compute -- curl -s localhost:8080/metrics | grep dhatu_texts_processed_total

echo "📈 Grafana Dashboard: http://grafana.dhatu-processing.local"
echo "🔍 Prometheus: http://prometheus.dhatu-processing.local"
