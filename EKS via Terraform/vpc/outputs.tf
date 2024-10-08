output "rds_subnet_ids" {
  value = [aws_subnet.rds_a.id, aws_subnet.rds_b.id]
}

output "cluster_subnet_ids" {
  value = [aws_subnet.cluster_a.id, aws_subnet.cluster_b.id]
}

output "node_group_subnet_ids" {
  value = [aws_subnet.node_a.id, aws_subnet.node_b.id]
}

output "vpc_id" {
    value = aws_vpc.aline-financial.id
}

output "rds_sec_group_id" {
  value = [aws_security_group.rds_sec_group.id]
}