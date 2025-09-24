terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}


provider "aws" {
  region = "us-east-1"
  
  default_tags {
    tags = {
      Project     = "finops-demo-free"
      Environment = "demo"
      CostCenter  = "free-tier"
      ManagedBy   = "terraform"
    }
  }
}
