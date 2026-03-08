variable "aws_region" {
  description = "Region de AWS donde se despliegan los recursos"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Nombre del proyecto, usado como prefijo en los recursos"
  type        = string
  default     = "flight-reservation"
}

variable "environment" {
  description = "Ambiente de despliegue (dev, staging, prod)"
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "El ambiente debe ser dev, staging o prod."
  }
}

variable "vpc_cidr" {
  description = "CIDR block para la VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "kubernetes_version" {
  description = "Version de Kubernetes para el cluster EKS"
  type        = string
  default     = "1.28"
}

variable "node_instance_type" {
  description = "Tipo de instancia EC2 para los nodos del cluster"
  type        = string
  default     = "t3.medium"
}

variable "node_min_size" {
  description = "Numero minimo de nodos en el node group"
  type        = number
  default     = 2
}

variable "node_max_size" {
  description = "Numero maximo de nodos en el node group"
  type        = number
  default     = 5
}

variable "node_desired_size" {
  description = "Numero deseado de nodos en el node group"
  type        = number
  default     = 3
}

variable "tags" {
  description = "Tags adicionales para todos los recursos"
  type        = map(string)
  default     = {}
}
