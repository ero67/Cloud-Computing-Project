# terraform/outputs.tf

output "gcs_bucket_name" {
  value = module.storage.bucket_name
}

output "gcs_bucket_url" {
  value = module.storage.bucket_url
}

output "bigquery_dataset_id" {
  value = module.bigquery.dataset_id
}

output "bigquery_table_id" {
  value = module.bigquery.table_id
}