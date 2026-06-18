variable "project" { type = string }
variable "environment" { type = string }
variable "vpc_id" { type = string }
variable "private_subnet_ids" { type = list(string) }
resource "aws_db_subnet_group" "this" { name = "${var.project}-${var.environment}" subnet_ids = var.private_subnet_ids }
resource "aws_security_group" "db" { name = "${var.project}-${var.environment}-db" vpc_id = var.vpc_id }
resource "aws_db_instance" "postgres" { identifier = "${var.project}-${var.environment}" engine = "postgres" engine_version = "17" instance_class = "db.t4g.micro" allocated_storage = 50 db_subnet_group_name = aws_db_subnet_group.this.name vpc_security_group_ids = [aws_security_group.db.id] username = "fitforge" manage_master_user_password = true storage_encrypted = true backup_retention_period = 7 skip_final_snapshot = false }
resource "aws_secretsmanager_secret" "database_url" { name = "${var.project}/${var.environment}/database-url" }
output "database_url_secret_arn" { value = aws_secretsmanager_secret.database_url.arn }
