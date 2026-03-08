output "cluster_name" {
  description = "Nombre del cluster EKS"
  value       = aws_eks_cluster.this.name
}

output "cluster_endpoint" {
  description = "Endpoint del API server de EKS"
  value       = aws_eks_cluster.this.endpoint
}

output "cluster_certificate_authority" {
  description = "Certificado CA del cluster (base64)"
  value       = aws_eks_cluster.this.certificate_authority[0].data
}

output "cluster_arn" {
  description = "ARN del cluster EKS"
  value       = aws_eks_cluster.this.arn
}

output "cluster_security_group_id" {
  description = "ID del security group del cluster"
  value       = aws_security_group.cluster.id
}

output "node_security_group_id" {
  description = "ID del security group de los nodos"
  value       = aws_security_group.node.id
}

output "node_group_name" {
  description = "Nombre del managed node group"
  value       = aws_eks_node_group.this.node_group_name
}

output "node_group_arn" {
  description = "ARN del managed node group"
  value       = aws_eks_node_group.this.arn
}

output "node_role_arn" {
  description = "ARN del IAM role de los nodos"
  value       = aws_iam_role.node.arn
}

output "cluster_role_arn" {
  description = "ARN del IAM role del cluster"
  value       = aws_iam_role.cluster.arn
}

output "oidc_provider_arn" {
  description = "ARN del proveedor OIDC para IRSA"
  value       = aws_iam_openid_connect_provider.cluster.arn
}

output "oidc_provider_url" {
  description = "URL del proveedor OIDC (sin https://)"
  value       = replace(aws_eks_cluster.this.identity[0].oidc[0].issuer, "https://", "")
}

output "cluster_version" {
  description = "Version de Kubernetes del cluster"
  value       = aws_eks_cluster.this.version
}
