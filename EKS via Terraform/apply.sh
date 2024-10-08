#!/bin/zsh

export TF_VAR_db_username=$(aws secretsmanager get-secret-value --secret-id \
arn:aws:secretsmanager:us-east-1:654654226626:secret:aline-database-credentials-pFK9eP \
| python3 parse_secret.py username)

export TF_VAR_db_password=$(aws secretsmanager get-secret-value --secret-id \
arn:aws:secretsmanager:us-east-1:654654226626:secret:aline-database-credentials-pFK9eP \
| python3 parse_secret.py password)

terraform apply