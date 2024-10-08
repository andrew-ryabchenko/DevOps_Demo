variable "rds_subnet_ids" {
    type = list(string)
    nullable = false
}

variable "rds_sec_group_ids" {
    type = list(string)
    nullable = false
}

variable db_username {}

variable db_password {}