module "vpc" {
    source = "./vpc"
}

module "iam" {
    source = "./iam"
}

module "cluster" {
    source = "./cluster"

    cluster_name = "aline-financial-ar"
    cluster_role_arn = module.iam.cluster_role_arn
    cluster_subnet_ids = module.vpc.cluster_subnet_ids

    node_group_name = "main-node-group"
    node_role_arn = module.iam.node_role_arn
    node_group_subnet_ids = module.vpc.node_group_subnet_ids
}

module "rds" {
    source = "./rds"
    db_username = var.db_username
    db_password = var.db_password
    rds_subnet_ids = module.vpc.rds_subnet_ids
    rds_sec_group_ids = module.vpc.rds_sec_group_id
}

