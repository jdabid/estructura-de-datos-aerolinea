variable "project_name" {
  description = "Nombre del proyecto para prefijos de recursos"
  type        = string
}

variable "environment" {
  description = "Ambiente de despliegue (dev, staging, prod)"
  type        = string
}

variable "cluster_name" {
  description = "Nombre del cluster EKS"
  type        = string
}

variable "kubernetes_version" {
  description = "Version de Kubernetes para el cluster"
  type        = string
  default     = "1.28"
}

variable "vpc_id" {
  description = "ID de la VPC donde se despliega el cluster"
  type        = string
}

variable "private_subnet_ids" {
  description = "IDs de las subnets privadas para los nodos"
  type        = list(string)
}

variable "public_subnet_ids" {
  description = "IDs de las subnets publicas para el endpoint del cluster"
  type        = list(string)
}

variable "node_instance_type" {
  description = "Tipo de instancia EC2 para los nodos"
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

variable "node_disk_size" {
  description = "Tamano del disco en GB para los nodos"
  type        = number
  default     = 50
}

variable "cluster_endpoint_public_access" {
  description = "Habilitar acceso publico al endpoint del cluster"
  type        = bool
  default     = true
}

variable "cluster_endpoint_private_access" {
  description = "Habilitar acceso privado al endpoint del cluster"
  type        = bool
  default     = true
}

variable "tags" {
  description = "Tags adicionales para los recursos"
  type        = map(string)
  default     = {}
}
