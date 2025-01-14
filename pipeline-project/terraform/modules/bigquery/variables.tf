# terraform/modules/bigquery/variables.tf

variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "dataset_id" {
  description = "BigQuery Dataset ID"
  type        = string
}

variable "dataset_location" {
  description = "Location for the BigQuery dataset"
  type        = string
}