output "all_backend_public_ips" {
  description = "Public IPs of all backend instances."
  value       = [for instance in aws_instance.backend_servers : instance.public_ip]
}

output "all_backend_public_dns" {
  description = "Public DNS names of all backend instances."
  value       = [for instance in aws_instance.backend_servers : instance.public_dns]
}

output "s3_bucket_name" {
  description = "Name of the S3 bucket created."
  value       = aws_s3_bucket.app_bucket.id
}
