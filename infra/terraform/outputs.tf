# ---------------------------------------------------------------------------
# VPC Outputs
# ---------------------------------------------------------------------------
output "vpc_id" {
  description = "ID de la VPC creada"
  value       = module.vpc.vpc_id
}

output "vpc_cidr_block" {
  description = "CIDR block de la VPC"
  value       = module.vpc.vpc_cidr_block
}

output "public_subnet_ids" {
  description = "IDs de las subnets publicas"
  value       = module.vpc.public_subnet_ids
}

output "private_subnet_ids" {
  description = "IDs de las subnets privadas"
  value       = module.vpc.private_subnet_ids
}

# ---------------------------------------------------------------------------
# EKS Outputs
# ---------------------------------------------------------------------------
output "cluster_name" {
  description = "Nombre del cluster EKS"
  value       = module.eks.cluster_name
}

output "cluster_endpoint" {
  description = "Endpoint del API server de EKS"
  value       = module.eks.cluster_endpoint
}

output "cluster_certificate_authority" {
  description = "Certificado CA del cluster EKS (base64)"
  value       = module.eks.cluster_certificate_authority
  sensitive   = true
}

output "cluster_security_group_id" {
  description = "ID del security group del cluster EKS"
  value       = module.eks.cluster_security_group_id
}

output "oidc_provider_arn" {
  description = "ARN del proveedor OIDC para IRSA"
  value       = module.eks.oidc_provider_arn
}

output "oidc_provider_url" {
  description = "URL del proveedor OIDC (sin https://)"
  value       = module.eks.oidc_provider_url
}

output "node_group_name" {
  description = "Nombre del managed node group"
  value       = module.eks.node_group_name
}

output "kubeconfig_command" {
  description = "Comando para configurar kubectl"
  value       = "aws eks update-kubeconfig --region ${var.aws_region} --name ${module.eks.cluster_name}"
}
