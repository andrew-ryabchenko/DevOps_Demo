#!/bin/zsh

ansible-playbook -i inventory.aws_ec2.yaml --key-file andrew.pem playbook.yaml