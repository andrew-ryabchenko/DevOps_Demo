output "host_ips" {
  value = [
     {
      uname = "ubuntu"
      host = aws_instance.ubuntu.public_ip
    },
    {
      uname = "ec2-user"
      host = aws_instance.rhel.public_ip
    },
    {
      uname = "ec2-user"
      host = aws_instance.al2.public_ip
    }
  ]
}