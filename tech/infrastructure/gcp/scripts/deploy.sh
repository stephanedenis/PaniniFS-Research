#!/bin/bash
set -e

echo "🚀 Deploying Dhātu Processing Infrastructure"
echo "Provider: gcp"
echo "Region: us-central1"

# Check prerequisites
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is required but not installed"
    exit 1
fi

if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is required but not installed"
    exit 1
fi

# Deploy infrastructure based on provider
case "gcp" in
    "aws")
        echo "☁️ Deploying AWS infrastructure..."
        aws cloudformation deploy \
            --template-body file://aws-infrastructure.json \
            --stack-name dhatu-processing-stack \
            --capabilities CAPABILITY_IAM \
            --region us-central1
        ;;
    "azure")
        echo "☁️ Deploying Azure infrastructure..."
        az deployment group create \
            --resource-group dhatu-processing-rg \
            --template-file azure-infrastructure.json
        ;;
    "gcp")
        echo "☁️ Deploying GCP infrastructure..."
        gcloud deployment-manager deployments create dhatu-processing \
            --config gcp-infrastructure.yaml
        ;;
    *)
        echo "❌ Unknown provider: gcp"
        exit 1
        ;;
esac

# Deploy Kubernetes manifests
echo "☸️ Deploying Kubernetes applications..."
kubectl apply -f k8s/

echo "✅ Deployment completed successfully!"
echo "📊 Monitor at: http://grafana.dhatu-processing.local"
