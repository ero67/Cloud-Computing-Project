output "dataset_id" {
  value = google_bigquery_dataset.pipeline_dataset.dataset_id
}

output "table_id" {
  value = google_bigquery_table.processed_data.table_id
}