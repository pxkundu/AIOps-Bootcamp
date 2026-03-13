# --- IDP Platform on AWS: ECS Fargate + ALB + RDS ---
# Serverless container deployment for the Knowledge Graph IDP portal.

terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

provider "aws" { region = var.aws_region }

# ============================================================
# VARIABLES
# ============================================================

variable "aws_region"    { default = "us-east-1" }
variable "project_name"  { default = "kg-idp" }
variable "db_password"   { type = string; sensitive = true }

# ============================================================
# NETWORKING
# ============================================================

resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = { Name = "${var.project_name}-vpc" }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id
  tags   = { Name = "${var.project_name}-igw" }
}

resource "aws_subnet" "public_a" {
  vpc_id = aws_vpc.main.id; cidr_block = "10.0.1.0/24"
  availability_zone = "${var.aws_region}a"; map_public_ip_on_launch = true
  tags = { Name = "${var.project_name}-pub-a" }
}

resource "aws_subnet" "public_b" {
  vpc_id = aws_vpc.main.id; cidr_block = "10.0.2.0/24"
  availability_zone = "${var.aws_region}b"; map_public_ip_on_launch = true
  tags = { Name = "${var.project_name}-pub-b" }
}

resource "aws_subnet" "private_a" {
  vpc_id = aws_vpc.main.id; cidr_block = "10.0.10.0/24"
  availability_zone = "${var.aws_region}a"
  tags = { Name = "${var.project_name}-priv-a" }
}

resource "aws_subnet" "private_b" {
  vpc_id = aws_vpc.main.id; cidr_block = "10.0.11.0/24"
  availability_zone = "${var.aws_region}b"
  tags = { Name = "${var.project_name}-priv-b" }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  route { cidr_block = "0.0.0.0/0"; gateway_id = aws_internet_gateway.igw.id }
  tags = { Name = "${var.project_name}-public-rt" }
}

resource "aws_route_table_association" "a" {
  subnet_id = aws_subnet.public_a.id; route_table_id = aws_route_table.public.id
}
resource "aws_route_table_association" "b" {
  subnet_id = aws_subnet.public_b.id; route_table_id = aws_route_table.public.id
}

# ============================================================
# SECURITY GROUPS
# ============================================================

resource "aws_security_group" "alb_sg" {
  name = "${var.project_name}-alb-sg"; vpc_id = aws_vpc.main.id
  ingress { from_port = 80; to_port = 80; protocol = "tcp"; cidr_blocks = ["0.0.0.0/0"] }
  ingress { from_port = 443; to_port = 443; protocol = "tcp"; cidr_blocks = ["0.0.0.0/0"] }
  egress  { from_port = 0; to_port = 0; protocol = "-1"; cidr_blocks = ["0.0.0.0/0"] }
}

resource "aws_security_group" "ecs_sg" {
  name = "${var.project_name}-ecs-sg"; vpc_id = aws_vpc.main.id
  ingress { from_port = 5005; to_port = 5005; protocol = "tcp"; security_groups = [aws_security_group.alb_sg.id] }
  egress  { from_port = 0; to_port = 0; protocol = "-1"; cidr_blocks = ["0.0.0.0/0"] }
}

resource "aws_security_group" "rds_sg" {
  name = "${var.project_name}-rds-sg"; vpc_id = aws_vpc.main.id
  ingress { from_port = 5432; to_port = 5432; protocol = "tcp"; security_groups = [aws_security_group.ecs_sg.id] }
  egress  { from_port = 0; to_port = 0; protocol = "-1"; cidr_blocks = ["0.0.0.0/0"] }
}

# ============================================================
# RDS POSTGRESQL
# ============================================================

resource "aws_db_subnet_group" "rds" {
  name       = "${var.project_name}-rds-subnets"
  subnet_ids = [aws_subnet.private_a.id, aws_subnet.private_b.id]
}

resource "aws_db_instance" "postgres" {
  identifier           = "${var.project_name}-db"
  engine               = "postgres"; engine_version = "16.4"
  instance_class       = "db.t3.micro"
  allocated_storage    = 20; storage_encrypted = true
  db_name              = "knowledgegraph"
  username             = "kgadmin"; password = var.db_password
  db_subnet_group_name = aws_db_subnet_group.rds.name
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  skip_final_snapshot  = true; publicly_accessible = false
  tags = { Name = "${var.project_name}-postgres" }
}

# ============================================================
# ECS FARGATE
# ============================================================

resource "aws_ecs_cluster" "main" {
  name = "${var.project_name}-cluster"
}

resource "aws_iam_role" "ecs_execution_role" {
  name = "${var.project_name}-ecs-exec-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{ Action = "sts:AssumeRole"; Effect = "Allow"; Principal = { Service = "ecs-tasks.amazonaws.com" } }]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_exec_policy" {
  role       = aws_iam_role.ecs_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_cloudwatch_log_group" "ecs" {
  name              = "/ecs/${var.project_name}"
  retention_in_days = 14
}

resource "aws_ecs_task_definition" "portal" {
  family                   = "${var.project_name}-portal"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "512"; memory = "1024"
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn

  container_definitions = jsonencode([{
    name  = "idp-portal"
    image = "python:3.12-slim"
    portMappings = [{ containerPort = 5005, hostPort = 5005, protocol = "tcp" }]
    environment = [
      { name = "DB_HOST", value = aws_db_instance.postgres.address },
      { name = "DB_NAME", value = "knowledgegraph" },
      { name = "DB_USER", value = "kgadmin" },
    ]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = aws_cloudwatch_log_group.ecs.name
        "awslogs-region"        = var.aws_region
        "awslogs-stream-prefix" = "portal"
      }
    }
  }])
}

resource "aws_ecs_service" "portal" {
  name            = "${var.project_name}-portal-svc"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.portal.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = [aws_subnet.public_a.id, aws_subnet.public_b.id]
    security_groups  = [aws_security_group.ecs_sg.id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.portal.arn
    container_name   = "idp-portal"
    container_port   = 5005
  }
}

# ============================================================
# APPLICATION LOAD BALANCER
# ============================================================

resource "aws_lb" "main" {
  name               = "${var.project_name}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets            = [aws_subnet.public_a.id, aws_subnet.public_b.id]
}

resource "aws_lb_target_group" "portal" {
  name        = "${var.project_name}-portal-tg"
  port        = 5005; protocol = "HTTP"
  vpc_id      = aws_vpc.main.id; target_type = "ip"
  health_check { path = "/api/stats"; interval = 30 }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
  port = 80; protocol = "HTTP"
  default_action { type = "forward"; target_group_arn = aws_lb_target_group.portal.arn }
}

# ============================================================
# OUTPUTS
# ============================================================

output "alb_url"       { value = "http://${aws_lb.main.dns_name}" }
output "rds_endpoint"  { value = aws_db_instance.postgres.endpoint }
output "ecs_cluster"   { value = aws_ecs_cluster.main.name }
