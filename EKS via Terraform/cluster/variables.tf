variable "cluster_name" {
    type = string
    default = "aline-financial-ar"
}

variable "cluster_role_arn" {
    type = string
    nullable = false
}

variable "cluster_subnet_ids" {
    type = list(string)
    nullable = false

    validation {
      condition = length(var.cluster_subnet_ids) >= 2
      error_message = "EKS cluster requires at least 2 subnets"
    }
}

variable "node_group_name" {
    type = string
    default = "main-node-group"
}

variable "node_role_arn" {
    type = string
    nullable = false
}

variable "node_group_subnet_ids" {
    type = list(string)
    nullable = false

    validation {
      condition = length(var.node_group_subnet_ids) >= 2
      error_message = "EKS node group requires at least 2 subnets"
    }
}
