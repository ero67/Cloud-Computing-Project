# Kubernetes Infrastructure Documentation

## Overview
This document describes the Kubernetes infrastructure setup for our data pipeline project. The infrastructure consists of a Google Kubernetes Engine (GKE) cluster running Prefect for workflow orchestration, with connections to various Google Cloud Platform (GCP) services.

## How to access kubernetes cluster ?

1. Install Google Cloud SDK
   1. Run the command `gcloud version` to verify Google Cloud SDK is installed
   2. Run `gcloud components install kubectl`
2. Run: `gcloud auth login`
3. Run: `gcloud container clusters get-credentials cloud-computing-cluster --zone us-central1-c --project teak-gamma-442315-f8`

You can now use kubernetes on our cluster from your local shell

## Prerequisites
- Google Cloud SDK installed
- kubectl installed
- Access to GCP project: `teak-gamma-442315-f8`
- Kubernetes cluster created in GKE

## Infrastructure Components

### 1. Namespace
All project resources are isolated in the `data-pipeline` namespace.

### 2. Prefect Setup
The project uses two main Prefect components:
- Prefect Server: Orchestrates workflows and provides the UI
- Prefect Agent: Executes the actual workflows

### 3. GCP Service Account
A service account with necessary permissions for:
- Google Cloud Storage
- BigQuery
- Cloud SQL

## Directory Structure
```
k8s/
└── base/
    ├── namespace.yaml       # Namespace definition
    ├── prefect-server.yaml  # Prefect server deployment
    ├── prefect-agent.yaml   # Prefect agent deployment
    ├── config.yaml         # ConfigMap for environment variables
    └── kustomization.yaml  # Kustomize configuration
```

## Deployment Steps

### 1. Initial Setup
```bash
# Set the project
gcloud config set project teak-gamma-442315-f8

# Create and connect to the cluster (if not already done)
gcloud container clusters get-credentials [cluster-name] --zone=[zone]
```

### 2. Create Namespace and Base Resources
```bash
kubectl apply -k k8s/base
```

### 3. Verify Deployments
```bash
# Check all resources in the namespace
kubectl get all -n data-pipeline
```

## Access to Prefect Server locally
To access prefect server locally run `kubectl port-forward service/prefect-server -n data-pipeline 4200:4200`

## Service Account and Permissions

The infrastructure uses a GCP service account with the following roles:
- `roles/storage.admin`: For GCS access
- `roles/bigquery.dataEditor`: For BigQuery access
- `roles/cloudsql.client`: For Cloud SQL access

The service account key is stored as a Kubernetes secret and mounted in the Prefect agent pod.

## Resource Management

Resources are configured with the following limits:
- Prefect Agent:
  - Requests: 256Mi memory, 100m CPU
  - Limits: 512Mi memory, 200m CPU

## Verification Steps

To verify the setup is working:

1. Check pod status:
```bash
kubectl get pods -n data-pipeline
```

2. Check Prefect server logs:
```bash
kubectl logs -n data-pipeline -l app=prefect-server
```

3. Check Prefect agent logs:
```bash
kubectl logs -n data-pipeline -l app=prefect-agent
```

## Common Operations

### Viewing Logs
```bash
# Server logs
kubectl logs -n data-pipeline -l app=prefect-server

# Agent logs
kubectl logs -n data-pipeline -l app=prefect-agent
```

### Scaling
To scale the number of Prefect agents:
```bash
kubectl scale deployment prefect-agent -n data-pipeline --replicas=2
```

### Updating Configurations
To apply configuration changes:
```bash
kubectl apply -k k8s/base
```

## Troubleshooting

### Common Issues

1. Pod in CrashLoopBackOff:
   - Check logs using `kubectl logs`
   - Verify resource limits
   - Check service account permissions

2. GCP Authentication Issues:
   - Verify secret mounting
   - Check service account key validity
   - Confirm IAM roles

### Useful Commands
```bash
# Get detailed pod information
kubectl describe pod [pod-name] -n data-pipeline

# Check mounted volumes
kubectl describe pod [pod-name] -n data-pipeline | grep -A 10 Volumes

# Check service account
kubectl describe pod [pod-name] -n data-pipeline | grep -A 5 "Service Account"
```


# Project Strucutre and Development
## Directory Structure
```
pipeline-project/
├── k8s/                      # Kubernetes configurations
│   └── base/                 # Base configurations
│       ├── namespace.yaml
│       ├── prefect-server.yaml
│       ├── prefect-agent.yaml
│       ├── config.yaml
│       └── kustomization.yaml
│
├── src/
│   ├── ingestion/           # Phase 2: Data Ingestion (Saddam)
│   │   ├── parquet_reader.py
│   │   └── tests/
│   │       └── test_gcp.py
│   │
│   ├── processing/          # Phase 3: Data Processing (Muhammad)
│   │   └── transformations/
│   │
│   └── visualization/       # Phase 4: Visualization (Dominik)
│       └── dashboards/
│
├── config/                  # Configuration files
│   └── prefect/            # Prefect workflow configurations
│
└── docs/                   # Documentation
    └── infrastructure/     # Infrastructure documentation
```
## Development Guidelines

### For Data Ingestion Development (Phase 2)
- Location: `src/ingestion/`
- Purpose: Handle Parquet file ingestion and GCS interactions
- Key Files:
  - `parquet_reader.py`: Implement Parquet file reading logic
  - Tests should be added in `tests/` directory

Example structure for a new ingestion component:

```python
# src/ingestion/parquet_reader.py
from google.cloud import storage

class ParquetReader:
    def __init__(self, bucket_name):
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.bucket(bucket_name)
        
    def read_parquet(self, file_path):
        # Implement parquet reading logic
        pass
```

### For Data Processing Development 
- Location: `src/processing/`
- Purpose: Transform data and load into BigQuery
- Create new transformations in `transformations/` directory

Example structure for a new transformation:
```python
# src/processing/transformations/data_transform.py
from google.cloud import bigquery

class DataTransformer:
    def __init__(self):
        self.bq_client = bigquery.Client()
        
    def transform_data(self, data):
        # Implement transformation logic
        pass
```

### For Visualization Development 
- Location: `src/visualization/`
- Purpose: Create dashboards and visualizations
- Store dashboard configurations in `dashboards/` directory


## GCS Bucket name
`data-pipeline-parquet-teak-gamma-442315-f8`