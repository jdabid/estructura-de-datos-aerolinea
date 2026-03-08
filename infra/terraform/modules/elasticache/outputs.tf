output "endpoint" {
  description = "Endpoint de conexion del cluster ElastiCache Redis"
  value       = aws_elasticache_cluster.main.cache_nodes[0].address
}

output "port" {
  description = "Puerto de conexion del cluster ElastiCache Redis"
  value       = aws_elasticache_cluster.main.cache_nodes[0].port
}

output "cluster_id" {
  description = "ID del cluster ElastiCache"
  value       = aws_elasticache_cluster.main.id
}

output "security_group_id" {
  description = "ID del security group de ElastiCache Redis"
  value       = aws_security_group.redis.id
}
