Minecraft Server Cluster on Kubernetes & Docker
A production-grade, auto-scaling Minecraft cluster with monitoring, backups, and security best practices.

Architecture Diagram Example Architecture: Kubernetes + Prometheus + Nginx

⭐ Features
Auto-Scaling: Dynamically scale servers based on real-time player count.

Zero Downtime: Load balancing via Nginx (Docker) or Kubernetes Ingress (Kubernetes).

Persistent Worlds: Automated backups to cloud storage (AWS S3, GCP Buckets).

Monitoring: Preconfigured dashboards (Grafana) for server health, player activity, and JVM metrics.

Security: RBAC, encrypted secrets, and network policies.

Multi-Cloud Ready: Deploy on AWS EKS, Google GKE, or local (Minikube).

🚀 Quick Start
Prerequisites
Docker & Docker Compose (for local testing)

Kubernetes Cluster (e.g., Minikube, EKS, GKE)

kubectl and helm installed

1. Local Deployment (Docker Compose)
bash
Copy
git clone https://github.com/Michael-ctrl-eng/Minecraft-Server-Cluster.git  
cd Minecraft-Server-Cluster  

# Start 2 servers + Nginx load balancer + Prometheus  
docker-compose up -d --scale minecraft=2  
Access Servers: localhost:25565 (load balanced across 2 instances).

2. Production Deployment (Kubernetes)
bash
Copy
# Deploy the cluster  
kubectl apply -f k8s/  

# Deploy monitoring stack (Prometheus + Grafana)  
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts  
helm install minecraft-monitoring prometheus-community/kube-prometheus-stack -f k8s/monitoring/values.yaml  
Access Grafana Dashboard:

bash
Copy
kubectl port-forward svc/minecraft-monitoring-grafana 3000:80  
# Open http://localhost:3000 (admin/password)  
🔧 Configuration
Environment Variables (Docker/Kubernetes)
Variable	Description	Default
EULA	Accept Minecraft EULA	TRUE
MEMORY	JVM Heap Size	2G
PLAYERS_MAX	Max players per server	20
BACKUP_INTERVAL	Cloud backup interval (minutes)	30
Example (Kubernetes Deployment):

yaml
Copy
env:  
- name: MEMORY  
  value: "4G"  
- name: BACKUP_INTERVAL  
  value: "15"  
Auto-Scaling
The cluster scales based on player count using Prometheus metrics and the Horizontal Pod Autoscaler (HPA):

Metrics Collection: A sidecar container in each Minecraft pod scrapes player count from server logs.

Prometheus Adapter: Translates custom metrics (players_active) for HPA.

Scaling Rule: Scale up if players_active > 15 per server for 5 minutes.

HPA Manifest:

yaml
Copy
apiVersion: autoscaling/v2  
kind: HorizontalPodAutoscaler  
metadata:  
  name: minecraft-hpa  
spec:  
  scaleTargetRef:  
    apiVersion: apps/v1  
    kind: Deployment  
    name: minecraft  
  minReplicas: 1  
  maxReplicas: 10  
  metrics:  
  - type: Pods  
    pods:  
      metric:  
        name: players_active  
      target:  
        type: AverageValue  
        averageValue: 15  
🔒 Security Best Practices
Network Policies: Restrict pod-to-pod traffic (see k8s/security/network-policies.yaml).

RBAC: Least-privilege service accounts for Prometheus and backups.

Secrets Management: Use Kubernetes Secrets or external vaults (e.g., AWS Secrets Manager).

Image Security: Scan Docker images with Trivy (make scan).

🗄️ Backup & Restore
Automated Backups:

CronJob backs up world data to S3/GCP every 30 minutes.

Enable in k8s/backups/backup-job.yaml:

yaml
Copy
- name: BACKUP_ENABLED  
  value: "true"  
- name: AWS_BUCKET  
  value: "s3://your-bucket"  
Restore a Snapshot:

bash
Copy
kubectl exec -it <minecraft-pod> -- /scripts/restore.sh s3://your-bucket/world-2023-10-01.tar.gz  
📊 Monitoring & Logging
Preconfigured Dashboards:

Grafana: Player activity, memory usage, and server latency.

Alerts: Slack/Discord notifications for high CPU or low disk space.

Grafana Dashboard

Log Aggregation:

bash
Copy
# Deploy Loki + Promtail for logs  
helm install loki grafana/loki-stack --values k8s/monitoring/loki-values.yaml  
🤝 Contributing
Fork the repo.

Test changes with make test (requires Terratest).

Submit a PR with updated docs and tests.

📜 License
Apache 2.0 - See LICENSE.
