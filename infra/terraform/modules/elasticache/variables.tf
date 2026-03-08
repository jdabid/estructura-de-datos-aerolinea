variable "project_name" {
  description = "Nombre del proyecto para etiquetado de recursos"
  type        = string
}

variable "environment" {
  description = "Ambiente de despliegue (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "vpc_id" {
  description = "ID del VPC donde se desplegara ElastiCache"
  type        = string
}

variable "private_subnet_ids" {
  description = "Lista de IDs de subnets privadas para el subnet group de ElastiCache"
  type        = list(string)
}

variable "eks_security_group_id" {
  description = "ID del security group de los nodos EKS para permitir acceso a Redis"
  type        = string
}

variable "node_type" {
  description = "Tipo de nodo de ElastiCache"
  type        = string
  default     = "cache.t3.micro"
}

variable "num_cache_nodes" {
  description = "Numero de nodos en el cluster de cache"
  type        = number
  default     = 1
}

variable "engine_version" {
  description = "Version del motor Redis"
  type        = string
  default     = "7.0"
}

variable "port" {
  description = "Puerto para conexiones Redis"
  type        = number
  default     = 6379
}

variable "snapshot_retention_limit" {
  description = "Dias de retencion de snapshots (0 desactiva snapshots)"
  type        = number
  default     = 0
}

variable "transit_encryption_enabled" {
  description = "Habilitar encriptacion en transito (TLS)"
  type        = bool
  default     = true
}

variable "tags" {
  description = "Tags adicionales para los recursos"
  type        = map(string)
  default     = {}
}
