output "instance_name" {
  value = google_sql_database_instance.instance.name
}

output "database_name" {
  value = google_sql_database.database.name
}

output "connection_name" {
  value = google_sql_database_instance.instance.connection_name
}