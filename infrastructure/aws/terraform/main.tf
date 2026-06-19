terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = ">= 5.0" }
  }
}

provider "aws" { region = var.aws_region }

module "network" { source = "./modules/network" project = var.project environment = var.environment }
module "data" { source = "./modules/data" project = var.project environment = var.environment vpc_id = module.network.vpc_id private_subnet_ids = module.network.private_subnet_ids }
module "ecs" { source = "./modules/ecs" project = var.project environment = var.environment vpc_id = module.network.vpc_id public_subnet_ids = module.network.public_subnet_ids private_subnet_ids = module.network.private_subnet_ids database_url_secret_arn = module.data.database_url_secret_arn }
