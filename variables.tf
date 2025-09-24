variable "region" {
  description = "AWS region para todos los recursos"
  type        = string
  default     = "us-east-1"  
}

variable "project_name" {
  description = "Nombre del proyecto demo"
  type        = string
  default     = "finops-demo-free"
}

variable "free_tier_limits" {
  description = "Límites de AWS Free Tier"
  type = map(number)
  default = {
    ec2_hours = 750
    s3_gb     = 5
  }
}

variable "lambda_stop_function_name" {
  description = "Nombre de la función Lambda para auto-stop"
  type        = string
  default     = "stop-demo-instances"
}
