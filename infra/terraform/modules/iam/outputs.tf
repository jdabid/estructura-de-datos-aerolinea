##############################################################################
# IAM Role ARNs
##############################################################################

output "api_role_arn" {
  description = "ARN del IAM role para el service account de flight-api"
  value       = aws_iam_role.api.arn
}

output "worker_role_arn" {
  description = "ARN del IAM role para el service account de flight-worker"
  value       = aws_iam_role.worker.arn
}

output "cicd_role_arn" {
  description = "ARN del IAM role para GitHub Actions CI/CD"
  value       = aws_iam_role.cicd.arn
}

##############################################################################
# ECR Repository URLs
##############################################################################

output "ecr_api_repository_url" {
  description = "URL del repositorio ECR para flight-api"
  value       = aws_ecr_repository.api.repository_url
}

output "ecr_frontend_repository_url" {
  description = "URL del repositorio ECR para flight-frontend"
  value       = aws_ecr_repository.frontend.repository_url
}

##############################################################################
# Service Account Annotations
##############################################################################

output "api_service_account_annotation" {
  description = "Anotacion para el service account de Kubernetes de flight-api"
  value       = "eks.amazonaws.com/role-arn: ${aws_iam_role.api.arn}"
}

output "worker_service_account_annotation" {
  description = "Anotacion para el service account de Kubernetes de flight-worker"
  value       = "eks.amazonaws.com/role-arn: ${aws_iam_role.worker.arn}"
}
