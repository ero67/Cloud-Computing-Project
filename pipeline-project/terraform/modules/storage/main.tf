resource "google_storage_bucket" "data_pipeline_bucket" {
  name     = var.bucket_name
  location = var.bucket_location
  labels = {
    environment = "development"
    project     = "data-pipeline"
    managed_by  = "terraform"
  }
  
  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition {
      age = 90
    }
    action {
      type = "Delete"
    }
  }
}

resource "google_storage_bucket_object" "folders" {
  for_each = toset(["raw/", "processed/", "archive/"])
  
  name    = each.key
  content = " "  # Empty content for folder creation
  bucket  = google_storage_bucket.data_pipeline_bucket.name
}
