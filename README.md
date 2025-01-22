Minecraft Server Cluster
Deploy Minecraft servers with Docker Compose or Kubernetes. Supports basic scaling, backups, and monitoring.

Docker+Kubernetes

📦 Features
Docker Compose Setup: Spin up Minecraft servers, Nginx load balancer, and Prometheus/Grafana locally.

Kubernetes Deployment: Deploy servers to a cluster with Horizontal Pod Autoscaling (HPA) based on CPU usage.

Basic Backups: Manual world data backup script (backup.sh).

Monitoring: Prometheus and Grafana included in Docker Compose for metrics.

🚀 Quick Start
Prerequisites
Docker & Docker Compose

Kubernetes cluster (e.g., Minikube, EKS)

kubectl

1. Local Deployment (Docker Compose)
bash
Copy
git clone https://github.com/Michael-ctrl-eng/Minecraft-Server-Cluster.git  
cd Minecraft-Server-Cluster  

# Start 1 Minecraft server + Nginx + Prometheus/Grafana  
docker-compose up -d  
Access Minecraft: localhost:25565

Grafana Dashboard: localhost:3000 (default: admin/admin)

2. Kubernetes Deployment
bash
Copy
kubectl apply -f k8s/  
Auto-Scaling: Servers scale based on CPU usage (default: scales at 50% CPU).

yaml
Copy
# k8s/hpa.yaml  
metrics:  
- type: Resource  
  resource:  
    name: cpu  
    target:  
      type: Utilization  
      averageUtilization: 50  
🔧 Configuration
Environment Variables
Variable	Description	Default
EULA	Accept Minecraft EULA	TRUE
MEMORY	JVM heap size (per server)	2G
SERVER_PORT	Minecraft server port	25565
Override in Docker Compose:

yaml
Copy
# docker-compose.yml  
environment:  
  - MEMORY=4G  
🗄️ Backups
Manually run the backup script to save world data:

bash
Copy
./backup.sh  
Backups are stored in backups/.

📊 Monitoring
Prometheus scrapes server metrics (port 9090).

Grafana comes preconfigured with a basic dashboard (port 3000).

⚠️ Limitations
Autoscaling: Currently scales on CPU usage, not player count.

Security: No RBAC, network policies, or encrypted secrets.

Backups: Manual script only—no automated cloud backups or CronJobs.

Tests: No automated validation for scaling/backups.

📜 License
MIT License. See LICENSE.
