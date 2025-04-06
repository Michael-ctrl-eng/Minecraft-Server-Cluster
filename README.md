MINECRAFT SERVER CLUSTER

A flexible and modern setup to run Minecraft servers using Docker Compose or Kubernetes. It supports scaling, manual backups, and performance monitoring.

Features
Docker Compose (Local Development):

Run Minecraft servers locally with Nginx as a load balancer.

Built-in Prometheus and Grafana for monitoring.

Kubernetes (Production Ready):

Deploy Minecraft servers to a Kubernetes cluster.

Horizontal Pod Autoscaler (HPA) adjusts the number of servers based on CPU usage.

Backups:

Manual backup script included to save world data.

Monitoring:

Prometheus collects metrics.

Grafana provides a pre-configured dashboard.

Quick Start
Requirements
Docker & Docker Compose

A Kubernetes cluster (e.g., Minikube, EKS)

kubectl

Local Deployment (Docker Compose)
bash
Copy
Edit
git clone https://github.com/Michael-ctrl-eng/Minecraft-Server-Cluster.git
cd Minecraft-Server-Cluster
docker-compose up -d
Minecraft: localhost:25565

Grafana: localhost:3000 (default login: admin/admin)

Kubernetes Deployment
bash
Copy
Edit
kubectl apply -f k8s/
Auto-scaling is handled via HPA and triggered by CPU usage. Example config:

yaml
Copy
Edit
metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
Configuration
Variable	Description	Default
EULA	Accept Minecraft EULA	TRUE
MEMORY	JVM heap size per server	2G
SERVER_PORT	Minecraft server port	25565
You can override variables in docker-compose.yml:

yaml
Copy
Edit
environment:
  MEMORY: 4G
Backups
To save the current world state, run:

bash
Copy
Edit
./backup.sh
Backups are saved in the backups/ directory.

Monitoring
Prometheus scrapes server metrics on port 9090.

Grafana dashboard available on port 3000.

Limitations
Autoscaling is based on CPU usage, not number of players.

No built-in security (RBAC, network policies, or encrypted secrets).

Backup process is manual only.

No automated tests for scaling or backup validation.

License
MIT License.

