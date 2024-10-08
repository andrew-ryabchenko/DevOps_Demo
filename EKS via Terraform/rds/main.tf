resource "aws_db_subnet_group" "default" {
    name       = "rds_subnet_group_ar"
    subnet_ids = var.rds_subnet_ids
}

resource "aws_db_instance" "database" {
    allocated_storage = 10
    db_subnet_group_name = aws_db_subnet_group.default.name
    engine = "mysql"
    instance_class = "db.m5d.large"
    vpc_security_group_ids = var.rds_sec_group_ids
    publicly_accessible = false
    skip_final_snapshot = true
    username = var.db_username
    password = var.db_password
    db_name = "aline_financial"
}
