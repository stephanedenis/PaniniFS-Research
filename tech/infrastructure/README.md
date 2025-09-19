# Dhātu Processing Cloud Deployment Guide

## Overview

This infrastructure as code package provides automated deployment for the Dhātu Processing system across AWS, Azure, and GCP with the following features:

- **Auto-scaling compute clusters** (CPU + GPU nodes)
- **Container orchestration** with Kubernetes
- **Monitoring and alerting** with Prometheus + Grafana
- **Cost optimization** with spot instances and auto-shutdown
- **Multi-cloud support** for vendor flexibility

## Performance Targets

- **Throughput**: 15,000+ texts/second (CPU optimized)
- **Scaling**: 2-20 CPU nodes, 1-8 GPU nodes
- **Memory**: Optimized streaming for 1M+ article corpora
- **Latency**: <100ms per text processing

## Quick Start

### AWS Deployment
```bash
cd infrastructure/aws
./scripts/deploy.sh
```

### Azure Deployment  
```bash
cd infrastructure/azure
./scripts/deploy.sh
```

### GCP Deployment
```bash
cd infrastructure/gcp
./scripts/deploy.sh
```

## Architecture

```
Internet
    ↓
Load Balancer
    ↓
┌─────────────┬─────────────┬─────────────┐
│ Coordinator │ CPU Compute │ GPU Compute │
│   Nodes     │    Nodes    │    Nodes    │
│  (2 min)    │  (2-20)     │   (1-8)     │
└─────────────┴─────────────┴─────────────┘
    ↓
Storage Layer
```

## Monitoring

- **Grafana**: Performance dashboards
- **Prometheus**: Metrics collection
- **Alerts**: CPU, memory, throughput monitoring

## Scaling

### Manual Scaling
```bash
./scripts/scale.sh cpu-compute 10
./scripts/scale.sh gpu-compute 4
```

### Auto-scaling
- CPU utilization > 70% → scale up
- CPU utilization < 30% → scale down
- Memory pressure → add nodes
- Queue depth → horizontal scaling

## Cost Optimization

- **Spot instances**: 50-70% cost reduction
- **Auto-shutdown**: Scale to zero during idle
- **Resource limits**: Memory and CPU boundaries
- **Multi-AZ**: Availability vs cost balance

## Security

- **Network isolation**: Private subnets
- **Access control**: IAM roles and RBAC
- **Encryption**: At rest and in transit
- **Secrets management**: Cloud native vaults

## Generated: 2025-09-19 10:51:58
