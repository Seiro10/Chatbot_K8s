terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region  = "eu-west-3"
  profile = "terraform-admin"
}

module "iam" {
  source = "./modules/iam"
}

module "vpc" {
  source          = "./modules/vpc"
  vpc_cidr        = "10.0.0.0/16"
  public_subnets  = ["10.0.1.0/24", "10.0.2.0/24"]
  private_subnets = ["10.0.3.0/24", "10.0.4.0/24"]
  availability_zones = ["eu-west-3a", "eu-west-3b"]
  cluster_name    = "chatbot-cluster" 
}

module "eks" {
  source              = "./modules/eks"
  cluster_name        = "chatbot-cluster"
  role_arn            = module.iam.eks_cluster_role_arn
  worker_node_role_arn = module.iam.worker_node_role_arn
  subnet_ids   = module.vpc.private_subnet_ids
}

module "alb" {
  source          = "./modules/alb"
  vpc_id          = module.vpc.vpc_id 
  security_groups = [module.vpc.alb_security_group_id]
  subnets = module.vpc.public_subnet_ids 
}

module "secrets" {
  source = "./modules/secrets"
}

