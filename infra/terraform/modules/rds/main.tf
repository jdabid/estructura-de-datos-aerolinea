locals {
  name_prefix = "${var.project_name}-${var.environment}"

  common_tags = merge(var.tags, {
    Project     = var.project_name
    Environment = var.environment
    Module      = "rds"
    ManagedBy   = "terraform"
  })
}

# ------------------------------------------------------------------------------
# Security Group - Acceso PostgreSQL desde nodos EKS
# ------------------------------------------------------------------------------
resource "aws_security_group" "rds" {
  name        = "${local.name_prefix}-rds-sg"
  description = "Security group para RDS PostgreSQL - permite acceso desde EKS"
  vpc_id      = var.vpc_id

  ingress {
    description     = "PostgreSQL desde nodos EKS"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [var.eks_security_group_id]
  }

  egress {
    description = "Trafico de salida"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-rds-sg"
  })
}

# ------------------------------------------------------------------------------
# Subnet Group - Subnets privadas para RDS
# ------------------------------------------------------------------------------
resource "aws_db_subnet_group" "main" {
  name        = "${local.name_prefix}-rds-subnet-group"
  description = "Subnet group para RDS PostgreSQL en subnets privadas"
  subnet_ids  = var.private_subnet_ids

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-rds-subnet-group"
  })
}

# ------------------------------------------------------------------------------
# Parameter Group - Configuracion PostgreSQL con pgvector
# ------------------------------------------------------------------------------
resource "aws_db_parameter_group" "main" {
  name        = "${local.name_prefix}-pg15-params"
  family      = "postgres15"
  description = "Parameter group para PostgreSQL 15 con soporte pgvector"

  parameter {
    name         = "shared_preload_libraries"
    value        = "pg_stat_statements,vector"
    apply_method = "pending-reboot"
  }

  parameter {
    name         = "log_statement"
    value        = "mod"
    apply_method = "immediate"
  }

  parameter {
    name         = "log_min_duration_statement"
    value        = "1000"
    apply_method = "immediate"
  }

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-pg15-params"
  })
}

# ------------------------------------------------------------------------------
# RDS PostgreSQL Instance
# ------------------------------------------------------------------------------
resource "aws_db_instance" "main" {
  identifier = "${local.name_prefix}-postgres"

  # Motor y version
  engine         = "postgres"
  engine_version = "15"

  # Capacidad
  instance_class        = var.instance_class
  allocated_storage     = var.allocated_storage
  max_allocated_storage = var.max_allocated_storage
  storage_type          = "gp3"

  # Base de datos y credenciales
  db_name  = var.db_name
  username = var.db_username
  password = var.db_password

  # Red
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  publicly_accessible    = false
  multi_az               = var.multi_az

  # Parameter group
  parameter_group_name = aws_db_parameter_group.main.name

  # Backups
  backup_retention_period = var.backup_retention_period
  backup_window           = "03:00-04:00"

  # Mantenimiento
  maintenance_window = "sun:04:30-sun:05:30"

  # Encriptacion en reposo
  storage_encrypted = true
  kms_key_id        = var.kms_key_arn != "" ? var.kms_key_arn : null

  # Proteccion y eliminacion
  deletion_protection = var.deletion_protection
  skip_final_snapshot = var.skip_final_snapshot
  final_snapshot_identifier = var.skip_final_snapshot ? null : "${local.name_prefix}-postgres-final-snapshot"

  # Monitoreo
  performance_insights_enabled = true

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-postgres"
  })
}
