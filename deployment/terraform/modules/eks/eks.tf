resource "aws_eks_cluster" "chatbot_eks" {
  name     = var.cluster_name
  role_arn = var.role_arn 
  version  = "1.31"  # Stable Kubernetes version

  vpc_config {
    subnet_ids = var.subnet_ids
  }
}

resource "aws_eks_node_group" "chatbot_nodes" {
  cluster_name  = aws_eks_cluster.chatbot_eks.name
  node_group_name = "chatbot-nodes"
  node_role_arn = var.worker_node_role_arn
  subnet_ids    = var.subnet_ids

  scaling_config {
    desired_size = 2
    min_size     = 1
    max_size     = 3
  }

  ami_type       = "AL2_x86_64"
  instance_types = ["t3.medium"]

  tags = {
    Name = "chatbot-node-group"
  }
}
