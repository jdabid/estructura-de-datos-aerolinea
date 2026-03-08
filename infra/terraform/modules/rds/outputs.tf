output "endpoint" {
  description = "Endpoint de conexion de la instancia RDS PostgreSQL"
  value       = aws_db_instance.main.endpoint
}

output "address" {
  description = "Hostname de la instancia RDS (sin puerto)"
  value       = aws_db_instance.main.address
}

output "port" {
  description = "Puerto de conexion de la instancia RDS"
  value       = aws_db_instance.main.port
}

output "db_name" {
  description = "Nombre de la base de datos"
  value       = aws_db_instance.main.db_name
}

output "instance_id" {
  description = "Identificador de la instancia RDS"
  value       = aws_db_instance.main.id
}

output "security_group_id" {
  description = "ID del security group de RDS"
  value       = aws_security_group.rds.id
}
