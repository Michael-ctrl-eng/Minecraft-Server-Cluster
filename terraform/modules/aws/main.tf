resource "aws_eks_cluster" "minecraft_cluster" {
  name     = var.cluster_name
  role_arn = aws_iam_role.eks_cluster_role.arn
  version  = var.kubernetes_version

  vpc_config {
    subnet_ids = var.subnet_ids
  }

  # ... other EKS cluster configurations
}

resource "aws_eks_node_group" "minecraft_node_group" {
  cluster_name = aws_eks_cluster.minecraft_cluster.name
  node_group_name = "minecraft-nodes"
  node_role_arn  = aws_iam_role.eks_node_role.arn
  subnet_ids     = var.subnet_ids

  scaling_config {
    desired_size = var.node_count
    min_size     = var.min_node_count
    max_size     = var.max_node_count
  }
  # ... other node group configurations
}

# ... IAM roles, security groups, etc.
