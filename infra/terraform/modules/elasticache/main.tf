locals {
  name_prefix = "${var.project_name}-${var.environment}"

  common_tags = merge(var.tags, {
    Project     = var.project_name
    Environment = var.environment
    Module      = "elasticache"
    ManagedBy   = "terraform"
  })
}

# ------------------------------------------------------------------------------
# Security Group - Acceso Redis desde nodos EKS
# ------------------------------------------------------------------------------
resource "aws_security_group" "redis" {
  name        = "${local.name_prefix}-redis-sg"
  description = "Security group para ElastiCache Redis - permite acceso desde EKS"
  vpc_id      = var.vpc_id

  ingress {
    description     = "Redis desde nodos EKS"
    from_port       = var.port
    to_port         = var.port
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
    Name = "${local.name_prefix}-redis-sg"
  })
}

# ------------------------------------------------------------------------------
# Subnet Group - Subnets privadas para ElastiCache
# ------------------------------------------------------------------------------
resource "aws_elasticache_subnet_group" "main" {
  name        = "${local.name_prefix}-redis-subnet-group"
  description = "Subnet group para ElastiCache Redis en subnets privadas"
  subnet_ids  = var.private_subnet_ids

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-redis-subnet-group"
  })
}

# ------------------------------------------------------------------------------
# Parameter Group - Configuracion Redis 7
# ------------------------------------------------------------------------------
resource "aws_elasticache_parameter_group" "main" {
  name        = "${local.name_prefix}-redis7-params"
  family      = "redis7"
  description = "Parameter group para Redis 7"

  parameter {
    name  = "maxmemory-policy"
    value = "allkeys-lru"
  }

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-redis7-params"
  })
}

# ------------------------------------------------------------------------------
# ElastiCache Redis Cluster
# ------------------------------------------------------------------------------
resource "aws_elasticache_cluster" "main" {
  cluster_id = "${local.name_prefix}-redis"

  # Motor y version
  engine               = "redis"
  engine_version       = var.engine_version
  node_type            = var.node_type
  num_cache_nodes      = var.num_cache_nodes
  port                 = var.port
  parameter_group_name = aws_elasticache_parameter_group.main.name

  # Red
  subnet_group_name  = aws_elasticache_subnet_group.main.name
  security_group_ids = [aws_security_group.redis.id]

  # Encriptacion en transito
  transit_encryption_enabled = var.transit_encryption_enabled

  # Snapshots
  snapshot_retention_limit = var.snapshot_retention_limit

  # Mantenimiento
  maintenance_window = "sun:05:00-sun:06:00"

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-redis"
  })
}
