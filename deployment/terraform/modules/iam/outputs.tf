output "eks_cluster_role_arn" {
  value       = aws_iam_role.eks_cluster_role.arn
  description = "IAM role ARN for EKS cluster"
}

output "worker_node_role_arn" {
  value       = aws_iam_role.worker_nodes.arn
  description = "IAM role ARN for EKS worker nodes"
}
