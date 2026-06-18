variable "project" { type = string }
variable "environment" { type = string }
variable "vpc_id" { type = string }
variable "public_subnet_ids" { type = list(string) }
variable "private_subnet_ids" { type = list(string) }
variable "database_url_secret_arn" { type = string }
resource "aws_ecs_cluster" "this" { name = "${var.project}-${var.environment}" }
resource "aws_cloudwatch_log_group" "api" { name = "/ecs/${var.project}-${var.environment}/api" retention_in_days = 30 }
resource "aws_ecr_repository" "api" { name = "${var.project}/api" image_scanning_configuration { scan_on_push = true } }
resource "aws_ecr_repository" "web" { name = "${var.project}/admin-web" image_scanning_configuration { scan_on_push = true } }
output "cluster_name" { value = aws_ecs_cluster.this.name }
