variable "project_id" {
  description = "GCP Project ID"
  type        = string
  default     = "teak-gamma-442315-f8"
}

variable "region" {
  description = "Default region for resources"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "Default zone for resources"
  type        = string
  default     = "us-central1-c"
}

variable "db_user" {
  description = "Database user name"
  type        = string
  default     = "pipeline_user"
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}