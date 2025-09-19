#!/bin/bash

echo "🧹 Cleaning up Dhātu Processing Infrastructure"

# Delete Kubernetes resources
kubectl delete namespace dhatu-processing --ignore-not-found=true

# Delete cloud infrastructure
case "aws" in
    "aws")
        aws cloudformation delete-stack --stack-name dhatu-processing-stack --region us-west-2
        ;;
    "azure")
        az group delete --name dhatu-processing-rg --yes --no-wait
        ;;
    "gcp")
        gcloud deployment-manager deployments delete dhatu-processing --quiet
        ;;
esac

echo "✅ Cleanup initiated"
