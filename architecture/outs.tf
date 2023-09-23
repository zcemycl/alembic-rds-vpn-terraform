output "db_instance_endpt" {
  value = aws_db_instance.rds.endpoint
}

output "rds_password" {
  value     = random_password.aurora.result
  sensitive = true
}
