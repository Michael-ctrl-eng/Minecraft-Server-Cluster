module "minecraft_aws" {
  source = "../../modules/aws"

  region           = "us-east-1"
  cluster_name     = "my-minecraft-cluster"
  kubernetes_version = "1.24"
  subnet_ids       = ["subnet-0xxxxxxxxxxxxxxxxx", "subnet-0yyyyyyyyyyyyyyyyy"]
  node_count       = 3
  # ...
}

output "cluster_endpoint" {
  value = module.minecraft_aws.cluster_endpoint
}

output "kubeconfig" {
  value = module.minecraft_aws.kubeconfig
}
