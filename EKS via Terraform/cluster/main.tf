resource "aws_eks_cluster" "aline-financial" {
    name = var.cluster_name
    role_arn = var.cluster_role_arn
    vpc_config {
      subnet_ids = var.cluster_subnet_ids
    }
}

resource "aws_eks_node_group" "main_node_group" {
    cluster_name = var.cluster_name
    node_group_name = var.node_group_name
    node_role_arn = var.node_role_arn
    subnet_ids = var.node_group_subnet_ids
    scaling_config {
        desired_size = 2
        max_size     = 3
        min_size     = 1
    }
    update_config {
        max_unavailable = 1
    }
    capacity_type = "ON_DEMAND"

    disk_size = 10
    depends_on = [ aws_eks_cluster.aline-financial ]
    # depends_on = [ 
    #     aws_iam_role.cluster_role,
    #     aws_iam_role.node_role
    # ]
}
