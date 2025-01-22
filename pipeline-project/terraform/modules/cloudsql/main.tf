# Random suffix to ensure unique instance names
resource "random_id" "db_name_suffix" {
  byte_length = 4
}

# Create Cloud SQL instance
resource "google_sql_database_instance" "instance" {
  name             = "data-pipeline-${random_id.db_name_suffix.hex}"
  database_version = "POSTGRES_14"
  region           = var.region
  project          = var.project_id

  settings {
    tier = "db-custom-2-7680"

    ip_configuration {
      ipv4_enabled = true
    }

    backup_configuration {
      enabled = true
      start_time = "02:00"
    }
  }

  deletion_protection = true 
}

# Create database
resource "google_sql_database" "database" {
  name     = "pipeline_db"
  instance = google_sql_database_instance.instance.name
}

# Create user
resource "google_sql_user" "user" {
  name     = var.db_user
  instance = google_sql_database_instance.instance.name
  password = var.db_password
}