# --- Terraform Variables ---

variable "aws_region" {
  description = "AWS region for all resources"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project identifier for tagging"
  type        = string
  default     = "aiops-idp"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.large"
}

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "db_name" {
  description = "PostgreSQL database name"
  type        = string
  default     = "openwebui"
}

variable "db_username" {
  description = "PostgreSQL master username"
  type        = string
  default     = "idpadmin"
}

variable "db_password" {
  description = "PostgreSQL master password"
  type        = string
  sensitive   = true
}

variable "openai_api_key" {
  description = "OpenAI API Key for GPT-4o"
  type        = string
  sensitive   = true
}

variable "my_ip" {
  description = "Your public IP for SSH access (CIDR format, e.g., 1.2.3.4/32)"
  type        = string
}
