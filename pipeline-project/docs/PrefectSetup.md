# Prefect Data Pipeline Documentation

## Architecture Overview

This data pipeline is built using Prefect for workflow orchestration, running on Kubernetes. The system consists of several key components:

### Components

1. **Prefect Server**
   - Runs in Kubernetes as a deployment
   - Provides the UI and API endpoints
   - Tracks flow runs, task states, and scheduling
   - Configuration in `prefect-server.yaml`

2. **Prefect Worker**
   - Runs in Kubernetes as a deployment
   - Picks up flow runs from the work queue
   - Creates Kubernetes jobs for flow execution
   - Configuration in `prefect-worker.yaml`

3. **Flow Code**
   - Main flow defined in `taxi_data_flow.py`
   - Deployment configuration in `deploy.py`
   - Packaged in a Docker container

4. **Infrastructure Components**
   - Kubernetes namespace: `data-pipeline`
   - Service Account: `prefect-worker`
   - RBAC configurations for necessary permissions
   - GCP service account for cloud storage access

### Flow Architecture

```
[Prefect UI/API Server] <-> [Prefect Worker] <-> [Kubernetes Job (Flow Execution)]
                                                      |
                                                      v
                                            [GCP Cloud Storage]
```

## CI/CD Pipeline

### GitHub Actions Workflow

The Docker image building and pushing is automated through GitHub Actions. The workflow is triggered on:
- Push to main branch
- Pull requests to main branch
- Manual trigger (workflow_dispatch)

Specifically, it monitors changes in:
```yaml
paths:
  - 'pipeline-project/src/processing/**'
  - '.github/workflows/docker-build-push.yml'
```

### Workflow Steps
1. Code changes are pushed to the repository
2. GitHub Actions workflow is triggered
3. Docker image is built with updated code
4. Image is pushed to Google Container Registry (gcr.io)
5. Kubernetes automatically pulls the new image when creating flow run jobs

## Flow Implementation

### Main Flow Components (`taxi_data_flow.py`)

The flow processes taxi data through several tasks:

1. Download Parquet file
2. Extract data
3. Process dataframe
4. Upload to GCS
5. Load to BigQuery

### Deployment Process

1. **Build and Push Docker Image**
   ```dockerfile
   FROM python:3.9.5-slim
   ENV PYTHONUNBUFFERED=1
   ENV PYTHONDONTWRITEBYTECODE=1
   ENV PREFECT_API_URL="http://prefect-server:4200/api"
   COPY requirements.txt /requirements.txt
   RUN pip install --no-cache-dir -r /requirements.txt
   COPY flows/deploy.py /deploy.py
   COPY flows/taxi_data_flow.py /taxi_data_flow.py
   CMD ["python", "/deploy.py"]
   ```
   Building and pushing the image to Google Container Registry is done via GitHub pipeline on push to main

2. **Deploy Flow**
   ```python
   # deploy.py
    deployment = NY_Taxi_Data_Flow.to_deployment(
        name="taxi-data-flow",
        work_pool_name="k8s-pool",
        work_queue_name="default"
    )
    
    # Deploy the flow
    deployment.apply()
   ```

## Kubernetes Configuration

### Worker Configuration

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prefect-worker
  namespace: data-pipeline
spec:
  replicas: 1
  template:
    spec:
      serviceAccountName: prefect-worker
      containers:
      - name: prefect-worker
        image: prefecthq/prefect:3.1.12-python3.9-kubernetes
        command: ["prefect", "worker", "start"]
        args: ["-p", "k8s-pool"]
```

### Work Pool Configuration

The work pool is configured with specific settings for job creation:
- Namespace: data-pipeline
- Service Account: prefect-worker
- Volume mounts for GCP credentials
- Environment variables for authentication

## Running the Pipeline

1. **Prerequisites**
   - Kubernetes cluster running
   - GCP service account with necessary permissions
   - Required secrets and configmaps created

2. **Deployment Steps**
   ```bash
   # Apply Kubernetes configurations
   kubectl apply -f prefect-server.yaml
   kubectl apply -f prefect-worker.yaml
   kubectl apply -f prefect-rbac.yaml

   # Build and push Docker image
   docker build -t gcr.io/teak-gamma-442315-f8/taxi-flow:latest .
   docker push gcr.io/teak-gamma-442315-f8/taxi-flow:latest

   # Deploy the flow
   kubectl apply -f taxi-data-processing-job.yaml
   ```

3. **Accessing the UI**
   ```bash
   kubectl port-forward svc/prefect-server 4200:4200 -n data-pipeline
   ```
   Then access http://localhost:4200

## Monitoring and Maintenance

### Checking Logs
```bash
# Worker logs
kubectl logs -f -l app=prefect-worker -n data-pipeline

# Flow run logs
kubectl logs -f job/[flow-job-name] -n data-pipeline
```


## Future Improvements

1. Add monitoring with Prometheus/Grafana
2. Implement OpenTelemetry tracing
3. Add automated testing
4. Implement GitOps workflow
5. Add data quality checks
