#!/bin/bash
set -e

# Stop Minecraft server before restore
systemctl stop minecraft

# Restore Minecraft data from the latest snapshot
restic restore latest --target "{{ minecraft_server_directory }}/docker"

# Start Minecraft server after restore
systemctl start minecraft
