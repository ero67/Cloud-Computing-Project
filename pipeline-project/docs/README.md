# Data Pipeline Project

## Project Overview
This project implements a data pipeline using Prefect for workflow orchestration, running on Google Kubernetes Engine (GKE). The infrastructure is managed with Terraform, and deployments are automated through GitHub Actions.

## Project Structure
```
.
├── .github/
│   └── workflows/
│       ├── docker-build-push.yaml    # CI/CD for Docker image
│       ├── infrastructure.yaml       # Infrastructure deployment
│       └── terraform.yaml            # Terraform automation
│
├── pipeline-project/
│   ├── config/                      # Configuration files
│   │   
│   │
│   ├── docs/                        # Project documentation
│   │   ├── PrefectSetup.md
│   │   ├── README.md
│   │   └── Terraform.md
│   │
│   ├── k8s/                         # Kubernetes configurations
│   │   └── base/   
│   │       ├── cloudsql-proxy.yaml
│   │       ├── cloudsql-secret.yaml
│   │       ├── config.yaml
│   │       ├── connection-test-pod.yaml
│   │       ├── kustomization.yaml
│   │       ├── namespace.yaml
│   │       ├── prefect-rbac.yaml
│   │       ├── prefect-server.yaml
│   │       ├── prefect-worker.yaml
│   │       └── taxi-data-processing-job.yaml
│   │
│   ├── src/
│   │   └── processing/              # Data processing code
│   │       ├── flows/
│   │       │   ├── deploy.py        # Prefect deployment script
│   │       │   └── taxi_data_flow.py # Main data flow
│   │       ├── Dockerfile
│   │       ├── requirements.txt
│   │       └── tests/
│   │           └── test_connections.py
│   │
│   └── terraform/                   # Infrastructure as Code
│       ├── .terraform/
│       ├── modules/
│       │   ├── bigquery/           # BigQuery setup
│       │   ├── cloudsql/          # Cloud SQL setup
│       │   └── storage/           # GCS setup
│       ├── environments/
│       └── main.tf
```

## Infrastructure Setup

### How to access kubernetes cluster ?

1. Install Google Cloud SDK
   1. Run the command `gcloud version` to verify Google Cloud SDK is installed
   2. Run `gcloud components install kubectl`
2. Run: `gcloud auth login`
3. Run: `gcloud container clusters get-credentials cloud-computing-cluster --zone us-central1-c --project teak-gamma-442315-f8`

You can now use kubernetes on our cluster from your local shell

### Prerequisites
- Google Cloud SDK
- kubectl
- Terraform
- Access to GCP project: `teak-gamma-442315-f8`

### GCP Resources
The infrastructure is managed through Terraform and includes:
- Google Kubernetes Engine (GKE) cluster
- Cloud SQL instance
- BigQuery datasets
- Google Cloud Storage buckets

### Terraform Structure
```
terraform/
├── modules/
│   ├── bigquery/        # BigQuery resources
│   ├── cloudsql/        # Cloud SQL instance
│   └── storage/         # GCS bucket configuration
└── environments/        # Environment-specific configurations
```

## Kubernetes Setup

1. Install Google Cloud SDK
   1. Run the command `gcloud version` to verify Google Cloud SDK is installed
   2. Run `gcloud components install kubectl`
2. Run: `gcloud auth login`
3. Run: `gcloud container clusters get-credentials cloud-computing-cluster --zone us-central1-c --project teak-gamma-442315-f8`

You can now use kubernetes on our cluster from your local shell

### Deploy Infrastructure
```bash
# Apply base configurations
kubectl apply -k k8s/base
```

## Data Pipeline

### Components
1. **Prefect Server**
   - Orchestrates workflows
   - Provides UI for monitoring
   - Runs in the `data-pipeline` namespace

2. **Prefect Worker**
   - Executes workflow tasks
   - Handles job creation in Kubernetes

3. **Data Flow**
   - Downloads taxi data
   - Processes data using Pandas
   - Uploads to GCS
   - Loads into BigQuery

### Continuous Integration/Deployment
The project uses GitHub Actions for:
1. Building and pushing Docker images
2. Deploying infrastructure changes
3. Running automated tests (not done yet)

Workflows are triggered on:
- Push to main branch
- Pull requests
- Manual triggers


## Monitoring and Maintenance

### View Logs
```bash
# Prefect server logs
kubectl logs -n data-pipeline -l app=prefect-server

# Prefect worker logs
kubectl logs -n data-pipeline -l app=prefect-worker
```

### Common Operations
```bash
# Scale workers
kubectl scale deployment prefect-worker -n data-pipeline --replicas=2

# Check pod status
kubectl get pods -n data-pipeline
```

## Configuration

### GCS Bucket
- Name: `data-pipeline-parquet-teak-gamma-442315-f8`

### Environment Variables
Environment variables are managed through Kubernetes ConfigMaps and Secrets in the `data-pipeline` namespace.

## Security

### Service Accounts
- Kubernetes service account: `prefect-worker`
- GCP service account with roles:
  - Storage Admin
  - BigQuery Data Editor
  - Cloud SQL Client
  - GCR User

### Secrets Management
- GCP credentials stored as Kubernetes secrets
- Database credentials managed through secrets
- Secret mounting handled via Kubernetes volumes


## Future Improvements
1. Add monitoring with Prometheus/Grafana
2. Implement OpenTelemetry tracing
3. Add automated testing in CI/CD pipeline
4. Implement GitOps workflow
5. Add data quality checks