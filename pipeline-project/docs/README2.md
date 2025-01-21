# Data Pipeline Project

## Project Overview
This project implements a data pipeline using Prefect for workflow orchestration, running on Google Kubernetes Engine (GKE). The infrastructure is managed with Terraform, and deployments are automated through GitHub Actions.

```mermaid
graph TD
    %% Data Source
    DS[NYC Taxi Data Source] -->|Download Parquet| PF[Prefect Flow]
   
    subgraph "GitHub & CI/CD"
        GH[GitHub Repository] -->|Push| GA[GitHub Actions]
        GA -->|Build & Push| GCR[Google Container Registry]
        GA -->|Deploy| TF[Terraform]
    end
   
    subgraph "Google Cloud Platform"
        %% Kubernetes Cluster
        subgraph "GKE Cluster"
            subgraph "data-pipeline namespace"
                PS[Prefect Server] -->|Create Jobs| PW[Prefect Worker]
                PW -->|Run| PF
                PF -->|Store Raw| GCS
                PF -->|Store Processed| GCS2[GCS Processed]
                PF -->|Load| BQ[BigQuery]
                PF -.->|Future Use| SQL[Cloud SQL]
            end
        end
       
        %% GCP Services
        GCS[GCS Raw]
        BQ
        SQL
    end
   
    %% Infrastructure Management
    TF -->|Manage Infrastructure| GKE[GKE Cluster]
    TF -->|Create| GCS
    TF -->|Create| BQ
    TF -->|Create| SQL

    %% Data Flow
    classDef gcp fill:#4285F4,stroke:#333,stroke-width:2px,color:white;
    classDef k8s fill:#326CE5,stroke:#333,stroke-width:2px,color:white;
    classDef github fill:#24292E,stroke:#333,stroke-width:2px,color:white;
    classDef flow fill:#00DB8B,stroke:#333,stroke-width:2px,color:black;
   
    class GCS,BQ,SQL,GKE gcp;
    class PS,PW k8s;
    class GH,GA github;
    class PF flow;