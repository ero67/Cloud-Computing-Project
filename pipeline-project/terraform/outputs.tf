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

output "cloudsql_instance_name" {
  value = module.cloudsql.instance_name
}

output "cloudsql_connection_name" {
  value = module.cloudsql.connection_name
}