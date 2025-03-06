output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.chatbot_vpc.id
}

output "public_subnet_ids" {
  value       = aws_subnet.public[*].id 
  description = "List of public subnet IDs"
}

output "private_subnet_ids" {
  value       = aws_subnet.private[*].id
  description = "List of private subnet IDs"
}

output "alb_security_group_id" {
  description = "Security group for ALB"
  value       = aws_security_group.alb_sg.id
}
