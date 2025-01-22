#!/bin/bash
set -e

# Set Minecraft server directory
MINECRAFT_DIR="{{ minecraft_server_directory }}"

# Stop Minecraft server before backup
systemctl stop minecraft

# Perform the backup using Restic
restic backup \
  --verbose \
  "{{ minecraft_server_directory }}/docker/data/world" \
  "{{ minecraft_server_directory }}/docker/config/server.properties" \
  "{{ minecraft_server_directory }}/docker/data/plugins"

# Start Minecraft server after backup
systemctl start minecraft

# Optional: Prune old backups to save space
# restic forget --prune --keep-daily 7 --keep-weekly 4 --keep-monthly 12
