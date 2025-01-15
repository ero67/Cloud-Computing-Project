terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
  backend "gcs" {
    bucket = "terraform-state-teak-gamma-442315-f8"
    prefix = "terraform/state"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

module "storage" {
  source = "./modules/storage"
  
  project_id = var.project_id
  bucket_name = "data-pipeline-parquet-${var.project_id}"
  bucket_location = var.region
}

module "bigquery" {
  source = "./modules/bigquery"
  
  project_id = var.project_id
  dataset_id = "data_pipeline"
  dataset_location = var.region
}

module "cloudsql" {
  source = "./modules/cloudsql"
  
  project_id  = var.project_id
  region      = var.region
  db_user     = var.db_user
  db_password = var.db_password
}