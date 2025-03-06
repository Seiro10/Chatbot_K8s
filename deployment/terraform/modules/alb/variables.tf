variable "subnets" {
  description = "List of public subnet IDs where the ALB will be deployed"
  type        = list(string)
}

variable "vpc_id" {
  description = "VPC ID for ALB"
  type        = string
}

variable "security_groups" {
  description = "List of security group IDs for the ALB"
  type        = list(string)
}
