variable "region" {
  type        = string
  description = "The AWS region to deploy to."
}

variable "cluster_name" {
  type        = string
  description = "The name of the EKS cluster."
}

variable "kubernetes_version" {
  type        = string
  description = "The desired Kubernetes version for the EKS cluster."
}

variable "subnet_ids" {
  type        = list(string)
  description = "The subnet IDs for the EKS cluster and node group."
}

# ... other variables
