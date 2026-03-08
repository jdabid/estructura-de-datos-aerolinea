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
  description = "ID del VPC donde se desplegara la instancia RDS"
  type        = string
}

variable "private_subnet_ids" {
  description = "Lista de IDs de subnets privadas para el subnet group de RDS"
  type        = list(string)
}

variable "eks_security_group_id" {
  description = "ID del security group de los nodos EKS para permitir acceso a RDS"
  type        = string
}

variable "instance_class" {
  description = "Clase de instancia RDS"
  type        = string
  default     = "db.t3.medium"
}

variable "allocated_storage" {
  description = "Almacenamiento inicial en GB"
  type        = number
  default     = 20
}

variable "max_allocated_storage" {
  description = "Almacenamiento maximo para auto-scaling en GB"
  type        = number
  default     = 100
}

variable "db_name" {
  description = "Nombre de la base de datos inicial"
  type        = string
  default     = "flight_reservation"
}

variable "db_username" {
  description = "Nombre de usuario maestro de la base de datos"
  type        = string
  default     = "flight_admin"
  sensitive   = true
}

variable "db_password" {
  description = "Contrasena del usuario maestro de la base de datos"
  type        = string
  sensitive   = true
}

variable "multi_az" {
  description = "Habilitar Multi-AZ para alta disponibilidad"
  type        = bool
  default     = false
}

variable "backup_retention_period" {
  description = "Dias de retencion de backups automaticos"
  type        = number
  default     = 7
}

variable "deletion_protection" {
  description = "Habilitar proteccion contra eliminacion accidental"
  type        = bool
  default     = false
}

variable "skip_final_snapshot" {
  description = "Omitir snapshot final al eliminar la instancia"
  type        = bool
  default     = true
}

variable "kms_key_arn" {
  description = "ARN de la llave KMS para encriptacion en reposo (si es vacio, usa llave por defecto de AWS)"
  type        = string
  default     = ""
}

variable "tags" {
  description = "Tags adicionales para los recursos"
  type        = map(string)
  default     = {}
}
