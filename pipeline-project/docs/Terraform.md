# Terraform

## Overview
Our infrastructure is managed using Terraform, which provisions and maintains our GCP resources through code. This ensures consistent, version-controlled, and reproducible infrastructure deployments.

## Infrastructure Components
- Google Cloud Storage bucket for data pipeline
- BigQuery dataset and tables
- Required IAM configurations

## Directory Structure
```
pipeline-project/terraform/
├── main.tf              # Main Terraform configuration
├── variables.tf         # Variable definitions
├── outputs.tf          # Output definitions
└── modules/
    ├── storage/        # GCS bucket configuration
    │   ├── main.tf
    │   ├── variables.tf
    │   └── outputs.tf
    └── bigquery/       # BigQuery configuration
        ├── main.tf
        ├── variables.tf
        └── outputs.tf
    └── cloudsql/       # Cloud SQL configuration
        ├── main.tf
        ├── variables.tf
        └── outputs.tf
```

## CI/CD Pipeline
Infrastructure changes are managed through a GitHub Actions workflow that:
1. Validates Terraform configurations
2. Plans changes on Pull Requests
3. Applies changes when merged to main

### Making Infrastructure Changes
1. Create a new branch:
   ```bash
   git checkout -b feature/infrastructure-change
   ```

2. Make your changes to Terraform files

3. Create a Pull Request:
   ```bash
   git add .
   git commit -m "Description of infrastructure changes"
   git push origin feature/infrastructure-change
   ```

4. The CI pipeline will:
   - Validate your Terraform configurations
   - Generate and comment the plan on your PR
   - Apply changes automatically when merged to main

### Local Development
1. Install Terraform:
   ```bash
   sudo apt-get update
   sudo apt-get install -y gnupg software-properties-common curl
   curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
   echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
   sudo apt-get update
   sudo apt-get install terraform
   ```

2. Set up GCP credentials:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/key.json"
   ```

3. Initialize Terraform:
   ```bash
   cd pipeline-project/terraform
   terraform init
   ```

### Resources Created
1. GCS Bucket:
   - Name: `data-pipeline-parquet-teak-gamma-442315-f8`
   - Folders: raw/, processed/, archive/
   - Location: US-CENTRAL1

2. BigQuery:
   - Dataset: `data_pipeline`
   - Tables:
     - `processed_data`
3. Cloud SQL:
   - Instance Name: `data-pipeline-4039b51c`
   - Type: PostgreSQL 14
   - Location: us-central1
   - Configuration:
     - Tier: db-f1-micro
     - Automated backups enabled
     - High availability: disabled
     - Connection name: `teak-gamma-442315-f8:us-central1:data-pipeline-4039b51c`

Example of connection to database can be found in src/ingestion/tests/test_connections.py