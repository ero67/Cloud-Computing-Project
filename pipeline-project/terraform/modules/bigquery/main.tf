# terraform/modules/bigquery/main.tf

resource "google_bigquery_dataset" "pipeline_dataset" {
  dataset_id  = var.dataset_id
  location    = var.dataset_location
  description = "Dataset for data pipeline project"

  access {
    role          = "OWNER"
    special_group = "projectOwners"
  }
  
  access {
    role          = "READER"
    special_group = "projectReaders"
  }

  access {
    role          = "WRITER"
    special_group = "projectWriters"
  }
}

resource "google_bigquery_table" "processed_data" {
  dataset_id = google_bigquery_dataset.pipeline_dataset.dataset_id
  table_id   = "processed_data"

  schema = jsonencode([
    {
      name = "timestamp",
      type = "TIMESTAMP",
      mode = "REQUIRED",
      description = "Record timestamp"
    },
    {
      name = "data_value",
      type = "FLOAT",
      mode = "NULLABLE",
      description = "Processed data value"
    }
  ])
}
