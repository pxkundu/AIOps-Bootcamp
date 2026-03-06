# --- Terraform Outputs ---

output "ec2_public_ip" {
  description = "Public IP of the IDP Server"
  value       = aws_eip.server_ip.public_ip
}

output "ec2_public_dns" {
  description = "Public DNS of the IDP Server"
  value       = aws_instance.idp_server.public_dns
}

output "rds_endpoint" {
  description = "RDS PostgreSQL endpoint"
  value       = aws_db_instance.postgres.endpoint
}

output "openwebui_url" {
  description = "URL to access the IDP Platform"
  value       = "http://${aws_eip.server_ip.public_ip}"
}

output "ssh_command" {
  description = "SSH command to connect to the IDP Server"
  value       = "ssh -i ${var.project_name}-key.pem ubuntu@${aws_eip.server_ip.public_ip}"
}
