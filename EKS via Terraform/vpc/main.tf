resource "aws_vpc" "aline-financial" {
  cidr_block = "10.0.0.0/16"
  enable_dns_support = true
  enable_dns_hostnames = true
  tags = {
    Name = "vpc_ar"
  }
}

resource "aws_subnet" "cluster_a" {
  vpc_id = aws_vpc.aline-financial.id
  cidr_block = "10.0.0.0/19"
  availability_zone = "us-east-1a"
  tags = {
    Name = "subnet_ar"
  }
}

resource "aws_subnet" "cluster_b" {
  vpc_id = aws_vpc.aline-financial.id
  cidr_block = "10.0.32.0/19"
  availability_zone = "us-east-1b"
  tags = {
    Name = "subnet_ar"
  }
}

resource "aws_subnet" "node_a" {
  vpc_id = aws_vpc.aline-financial.id
  cidr_block = "10.0.64.0/19"
  availability_zone = "us-east-1a"
  map_public_ip_on_launch = true
  tags = {
    Name = "subnet_ar_node_a"
  }
}

resource "aws_subnet" "node_b" {
  vpc_id = aws_vpc.aline-financial.id
  cidr_block = "10.0.96.0/19"
  availability_zone = "us-east-1b"
  map_public_ip_on_launch = true
  tags = {
    Name = "subnet_ar_node_b"
  }
}

resource "aws_subnet" "rds_a" {
  vpc_id = aws_vpc.aline-financial.id
  cidr_block = "10.0.128.0/19"
  availability_zone = "us-east-1a"
  tags = {
    Name = "subnet_ar"
  }
}

resource "aws_subnet" "rds_b" {
  vpc_id = aws_vpc.aline-financial.id
  cidr_block = "10.0.160.0/19"
  availability_zone = "us-east-1b"
  tags = {
    Name = "subnet_ar"
  }
}

resource "aws_internet_gateway" "igw" {
    vpc_id = aws_vpc.aline-financial.id
}

resource "aws_route_table" "public_subnet_table" {
    vpc_id = aws_vpc.aline-financial.id
    route {
        cidr_block = "0.0.0.0/0"
        gateway_id = aws_internet_gateway.igw.id
      }
      tags = {
        Name = "rtable_ar"
      }
}

resource "aws_route_table_association" "rte_tbl_assoc_node_a" {
    subnet_id = aws_subnet.node_a.id
    route_table_id = aws_route_table.public_subnet_table.id
}

resource "aws_route_table_association" "rte_tbl_assoc_node_b" {
    subnet_id = aws_subnet.node_b.id
    route_table_id = aws_route_table.public_subnet_table.id
}

resource "aws_security_group" "rds_sec_group" {
  name = "rds_security_group"
  description = "Restricts inbound traffic to only port 3306"
  vpc_id = aws_vpc.aline-financial.id

  ingress {
    from_port = 3306
    to_port = 3306
    protocol = "TCP"
    cidr_blocks = [ "0.0.0.0/0" ]
  }
  tags = {
    Name = "secgroup_ar"
  }
}

resource "aws_network_acl" "pub_subnet_acl" {
  vpc_id = aws_vpc.aline-financial.id
  subnet_ids = [ aws_subnet.node_a.id,
                 aws_subnet.node_b.id ]
  ingress {
    rule_no    = 1
    protocol   = "6"
    action     = "allow"
    cidr_block = "10.0.0.0/16"
    from_port  = 22
    to_port    = 22
  }
  ingress {
    rule_no    = 2
    protocol   = "6"
    action     = "deny"
    cidr_block = "0.0.0.0/0"
    from_port  = 22
    to_port    = 22
  }
  ingress {
    rule_no    = 100
    protocol   = "-1"
    action     = "allow"
    from_port  = 0
    to_port    = 0
    cidr_block = "0.0.0.0/0"
  }
  egress {
    rule_no    = 100
    protocol   = "-1"
    action     = "allow"
    from_port  = 0
    to_port    = 0
    cidr_block = "0.0.0.0/0"
  }
  tags = {
    Name = "public_subnet_acl_ar"
  }
}
