variable "project" { type = string }
variable "environment" { type = string }
resource "aws_vpc" "this" { cidr_block = "10.40.0.0/16" enable_dns_support = true enable_dns_hostnames = true tags = { Name = "${var.project}-${var.environment}" } }
resource "aws_subnet" "public_a" { vpc_id = aws_vpc.this.id cidr_block = "10.40.1.0/24" map_public_ip_on_launch = true }
resource "aws_subnet" "public_b" { vpc_id = aws_vpc.this.id cidr_block = "10.40.2.0/24" map_public_ip_on_launch = true }
resource "aws_subnet" "private_a" { vpc_id = aws_vpc.this.id cidr_block = "10.40.11.0/24" }
resource "aws_subnet" "private_b" { vpc_id = aws_vpc.this.id cidr_block = "10.40.12.0/24" }
output "vpc_id" { value = aws_vpc.this.id }
output "public_subnet_ids" { value = [aws_subnet.public_a.id, aws_subnet.public_b.id] }
output "private_subnet_ids" { value = [aws_subnet.private_a.id, aws_subnet.private_b.id] }
