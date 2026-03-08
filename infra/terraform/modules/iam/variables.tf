variable "eks_oidc_provider_arn" {
  description = "ARN del OIDC provider del cluster EKS"
  type        = string
}

variable "eks_oidc_provider_url" {
  description = "URL del OIDC provider del cluster EKS (sin https://)"
  type        = string
}

variable "namespace" {
  description = "Namespace de Kubernetes donde se despliegan los workloads"
  type        = string
  default     = "flight-system"
}

variable "environment" {
  description = "Ambiente de despliegue (dev, staging, production)"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "production"], var.environment)
    error_message = "El ambiente debe ser dev, staging o production."
  }
}

variable "github_org" {
  description = "Organizacion de GitHub para la trust policy de CI/CD"
  type        = string
  default     = "jdabid"
}

variable "github_repo" {
  description = "Repositorio de GitHub para la trust policy de CI/CD"
  type        = string
  default     = "flight-reservation-system"
}

variable "tags" {
  description = "Tags adicionales para los recursos"
  type        = map(string)
  default     = {}
}
