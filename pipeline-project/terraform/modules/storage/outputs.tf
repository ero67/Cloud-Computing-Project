output "bucket_name" {
  value = google_storage_bucket.data_pipeline_bucket.name
}

output "bucket_url" {
  value = google_storage_bucket.data_pipeline_bucket.url
}