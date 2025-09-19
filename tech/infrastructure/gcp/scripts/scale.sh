#!/bin/bash

COMPONENT=$1
REPLICAS=$2

if [ -z "$COMPONENT" ] || [ -z "$REPLICAS" ]; then
    echo "Usage: $0 <component> <replicas>"
    echo "Components: cpu-compute, gpu-compute"
    exit 1
fi

echo "📈 Scaling $COMPONENT to $REPLICAS replicas"

case "$COMPONENT" in
    "cpu-compute")
        kubectl scale deployment dhatu-cpu-compute --replicas=$REPLICAS -n dhatu-processing
        ;;
    "gpu-compute")
        kubectl scale deployment dhatu-gpu-compute --replicas=$REPLICAS -n dhatu-processing
        ;;
    *)
        echo "❌ Unknown component: $COMPONENT"
        exit 1
        ;;
esac

echo "✅ Scaling completed"
