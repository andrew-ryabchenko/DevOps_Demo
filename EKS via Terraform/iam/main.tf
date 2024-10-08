resource "aws_iam_role" "cluster_role" {
    name = "default_cluster_role_ar"
    assume_role_policy = file("${path.module}/cluster-trust-policy.json")
    managed_policy_arns = [
        "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
    ]
}

resource "aws_iam_role" "node_role" {
    name = "default_node_role_ar"
    assume_role_policy = file("${path.module}/nodegroup-trust-policy.json")
    managed_policy_arns = [
        "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy",
        "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly",
        "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
    ]
}
