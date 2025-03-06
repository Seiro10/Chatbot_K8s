variable "cluster_name" {
  description = "Name of the EKS cluster"
  type        = string
}

variable "role_arn" {
  description = "IAM role for EKS"
  type        = string
}

variable "subnet_ids" {
  description = "List of subnet IDs for the EKS cluster"
  type        = list(string)
}

variable "worker_node_role_arn" {
  description = "IAM role ARN for EKS worker nodes"
  type        = string
}

