resource "aws_instance" "ubuntu" {
  ami                         = "ami-080e1f13689e07408"
  instance_type               = "t2.micro"
  key_name                    = "andrew"
  associate_public_ip_address = true
  subnet_id                   = "subnet-04d1d2d1f3d673824"
  vpc_security_group_ids      = ["sg-08dcb830311555135"]
  tags = {
    Name = "managed-node-ansible-ubuntu-ar"
    Type = "ansible-ubuntu-ar"
  }
}

resource "aws_instance" "rhel" {
  ami                         = "ami-0fe630eb857a6ec83"
  instance_type               = "t2.micro"
  key_name                    = "andrew"
  associate_public_ip_address = true
  subnet_id                   = "subnet-04d1d2d1f3d673824"
  vpc_security_group_ids      = ["sg-08dcb830311555135"]
  tags = {
    Name = "managed-node-ansible-rhel-ar"
    Type = "ansible-rhel-ar"
  }
}

resource "aws_instance" "al2" {
  ami                         = "ami-051f8a213df8bc089"
  instance_type               = "t2.micro"
  key_name                    = "andrew"
  associate_public_ip_address = true
  subnet_id                   = "subnet-04d1d2d1f3d673824"
  vpc_security_group_ids      = ["sg-08dcb830311555135"]
  tags = {
    Name = "managed-node-ansible-awslinux-ar"
    Type = "ansible-awslinux-ar"
  }
}
