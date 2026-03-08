variable "project_name" {
  description = "Nombre del proyecto para prefijos de recursos"
  type        = string
}

variable "environment" {
  description = "Ambiente de despliegue (dev, staging, prod)"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block para la VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "cluster_name" {
  description = "Nombre del cluster EKS para tags de descubrimiento"
  type        = string
}

variable "availability_zones_count" {
  description = "Numero de zonas de disponibilidad a utilizar"
  type        = number
  default     = 3
}

variable "tags" {
  description = "Tags adicionales para los recursos"
  type        = map(string)
  default     = {}
}
