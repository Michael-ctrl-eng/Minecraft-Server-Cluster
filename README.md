# Minecraft Server Cluster

This project deploys a highly available, scalable, and secure Minecraft Server cluster using Docker, Ansible, Elasticsearch, Logstash, Kibana, Prometheus, Grafana, and HAProxy.

## Architecture


## Prerequisites

*   **Servers:**  You will need several servers (at least 7 recommended for a highly available setup) with Ubuntu 20.04 or later installed.
*   **Ansible:** Ansible must be installed on your control machine (the machine from which you will run the Ansible playbooks).
*   **SSH Access:** You need SSH access to all servers with a user that has sudo privileges.
*   **Docker and Docker Compose:** Docker and Docker Compose should be preinstalled on all servers that will run Docker containers
*   **Certificates (for TLS):**  You will need to generate or obtain TLS certificates for Elasticsearch, Logstash, Kibana, and Filebeat.

## Deployment

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Michael-ctrl-eng/Minecraft-Server-Cluster.git
    cd Minecraft-Server-Cluster
    ```

2. **Install Ansible roles (if any):**

    ```bash
    ansible-galaxy install -r requirements.yml
    ```

3. **Configure Ansible:**
    *   Update `ansible/inventory.ini` with the IP addresses of your servers.
    *   Configure `ansible/group_vars/all.yml` with your desired settings (passwords, versions, etc.). **Use Ansible Vault to encrypt sensitive data.**
    *   Place your generated TLS certificates in the appropriate `files/certs` directories within each role.

4. **Run the Ansible playbook:**

    ```bash
    ansible-playbook -i ansible/inventory.ini ansible/playbook.yml
    ```

## Configuration

### Elasticsearch

*   **`es_version`:** The version of Elasticsearch to install.
*   **`es_heap_size`:** The JVM heap size for Elasticsearch.
*   **`es_data_dir`:** The directory where Elasticsearch will store its data.
*   **`es_security_enabled`:** Set to `true` to enable security features (TLS and authentication).
*   **`es_xpack_security_...`:**  Variables for configuring TLS. Provide paths to your keystores and truststores.
*   **`es_keystore_password`:**  The password for your Elasticsearch keystore (encrypted with Ansible Vault).

### Logstash

*   **`ls_version`:** The version of Logstash to install.
*   **`ls_heap_size`:** The JVM heap size for Logstash.
*   **`logstash_beats_ssl_enabled`:** Set to `true` to enable TLS for the Beats input.
*   **`logstash_password`:** The password for the `logstash_internal` user (encrypted with Ansible Vault).

### Kibana

*   **`kibana_version`:** The version of Kibana to install.
*   **`kibana_security_enabled`:** Set to `true` to enable TLS.
*   **`kibana_password`:** The password for the `kibana_user` (encrypted with Ansible Vault).

### Filebeat

*   **`filebeat_version`:** The version of Filebeat to install.
*   **`filebeat_logstash_ssl_enabled`:** Set to `true` to enable TLS for communication with Logstash.

### HAProxy

*   **`haproxy_stats_user`:** The username for accessing HAProxy stats.
*   **`haproxy_stats_password`:** The password for accessing HAProxy stats (encrypted with Ansible Vault).
*   **`haproxy_stats_port`:** The port for the HAProxy stats page.

### Keepalived 

*   **`keepalived_virtual_ip`:** The virtual IP address for HAProxy failover.
*   **`keepalived_interface`:** The network interface to use for Keepalived.

### Minecraft Server

*   **`minecraft_version`:** The version of the Minecraft server to install.
*   **`minecraft_server_jar_url`:** The download URL for the Minecraft server JAR.
*   **`minecraft_server_type`:** The type of Minecraft server (VANILLA, SPIGOT, PAPER, etc.).
*   **`minecraft_server_directory`:** The directory where the Minecraft server will be installed.
*   **`minecraft_user`:** The user that will run the Minecraft server.
*   **`minecraft_heap_size`:** The JVM heap size for the Minecraft server.
*   **`minecraft_max_players`:** The maximum number of players allowed on the server.
*   **`minecraft_motd`:** The message of the day.
*   **`rcon_password`:** The password for RCON access (encrypted with Ansible Vault).
*   **`online_mode`:** Set to `true` to enable online mode (authentication with Mojang servers).

### Backup

*   **`backup_enabled`:** Set to `true` to enable backups.
*   **`backup_location`:** The location where backups will be stored (local directory or S3 bucket).
*   **`restic_password`:** The password for the Restic repository (encrypted with Ansible Vault).

### Monitoring

*   **`prometheus_version`:** The version of Prometheus to install.
*   **`grafana_version`:** The version of Grafana to install.
*   **`node_exporter_version`:** The version of Node Exporter to install.
*   **`grafana_admin_password`:** The initial admin password for Grafana (encrypted with Ansible Vault).

## Operation

*   **Starting/Stopping Services:**  Use the `systemctl` command to manage services (e.g., `systemctl start elasticsearch`, `systemctl stop minecraft`).
*   **Monitoring:** Access Grafana at `http://<monitoring_server_ip>:3000` to view dashboards and monitor the cluster.
*   **Logs:** Access Kibana at `http://<kibana_server_ip>:5601` to view and analyze logs.
*   **HAProxy Stats:** Access the HAProxy stats page at `http://<haproxy_server_ip>:1936`.

## Security

*   **TLS:**  TLS encryption is enabled for communication between Elasticsearch, Logstash, Kibana, and Filebeat.
*   **Authentication:** User authentication is enforced for Elasticsearch and Kibana.
*   **Firewall:**  A firewall (UFW) is configured to restrict access to only necessary ports.
*   **Secrets Management:** Ansible Vault is used to encrypt sensitive data.

## Backup and Restore

*   Backups are automatically performed using `restic` and scheduled with `cron`.
*   The backup script is located at `{{ minecraft_server_directory }}/backup.sh`.
*   The restore script is located at `{{ minecraft_server_directory }}/restore.sh`.

## Troubleshooting

*   **Logs:** Check the logs of each service for errors:
    *   Elasticsearch: `/var/log/elasticsearch`
    *   Logstash: `/var/log/logstash`
    *   Kibana: `/var/log/kibana`
    *   Minecraft: `{{ minecraft_server_directory }}/logs`
    *   Filebeat: `/var/log/filebeat`
    *   HAProxy: `/var/log/haproxy.log`
    *   Prometheus: `/var/log/prometheus`
    *   Grafana: `/var/log/grafana`
*   **systemd:** Use `systemctl status <service>` to check the status of a service.
*   **Journalctl:** Use `journalctl -u <service>` to view the systemd journal for a service.

## Upgrading

*   To upgrade a component, update the corresponding version variable in `group_vars/all.yml` and re-run the Ansible playbook with the appropriate tag (e.g., `ansible-playbook -i ansible/inventory.ini ansible/playbook.yml --tags elasticsearch`).

## License

[MIT]
