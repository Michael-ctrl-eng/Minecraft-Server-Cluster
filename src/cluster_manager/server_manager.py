import logging
import subprocess
import time
from pydantic import BaseModel, validator
import redis

from src.cluster_manager.config import load_config
from src.cluster_manager.exceptions import (
    ServerStartError,
    ServerStopError,
    ServerNotFoundError,
)

config = load_config()
r = redis.Redis(
    host=config.redis.host, port=config.redis.port, db=config.redis.db
)

logger = logging.getLogger(__name__)

class Server(BaseModel):
    server_id: int
    status: str = "stopped"

    def start(self):
        """Starts the server."""
        if self.status == "running":
            raise ServerStartError(f"Server {self.server_id} is already running")

        logger.info(f"Starting server {self.server_id}...")
        try:
            # Simulate starting a server (replace with your actual start command)
            process = subprocess.Popen(
                ["start_server_command", str(self.server_id)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                logger.error(
                    f"Error starting server {self.server_id}: {stderr.decode()}"
                )
                raise ServerStartError(
                    f"Failed to start server {self.server_id}: {stderr.decode()}"
                )

            self.status = "running"
            update_server_registry(self)
            logger.info(f"Server {self.server_id} started successfully")

        except Exception as e:
            logger.error(f"An error occurred while starting server {self.server_id}: {e}")
            raise ServerStartError(f"Failed to start server {self.server_id}: {e}")

    def stop(self):
        """Stops the server."""
        if self.status == "stopped":
            raise ServerStopError(f"Server {self.server_id} is already stopped")

        logger.info(f"Stopping server {self.server_id}...")
        try:
            # Simulate stopping a server (replace with your actual stop command)
            process = subprocess.Popen(
                ["stop_server_command", str(self.server_id)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                logger.error(
                    f"Error stopping server {self.server_id}: {stderr.decode()}"
                )
                raise ServerStopError(
                    f"Failed to stop server {self.server_id}: {stderr.decode()}"
                )

            self.status = "stopped"
            update_server_registry(self)
            logger.info(f"Server {self.server_id} stopped successfully")

        except Exception as e:
            logger.error(f"An error occurred while stopping server {self.server_id}: {e}")
            raise ServerStopError(f"Failed to stop server {self.server_id}: {e}")

    def get_status(self):
        """Gets the current status of the server."""
        return self.status

def get_server(server_id: int) -> Server:
    """Retrieves a server from the registry.

    Args:
        server_id: The ID of the server to retrieve.

    Returns:
        The Server object.

    Raises:
        ServerNotFoundError: If the server is not found in the registry.
    """
    server_data = r.hgetall(f"server:{server_id}")
    if not server_data:
        raise ServerNotFoundError(f"Server {server_id} not found")

    return Server(
        server_id=server_id,
        status=server_data[b"status"].decode(),
    )

def update_server_registry(server: Server):
    """Updates the server registry with the current server status."""
    r.hset(f"server:{server.server_id}", "status", server.status)

def start_server(server_id: int):
    """Starts a server.

    Args:
        server_id: The ID of the server to start.
    """
    try:
        server = get_server(server_id)
    except ServerNotFoundError:
        server = Server(server_id=server_id)
    server.start()

def stop_server(server_id: int):
    """Stops a server.

    Args:
        server_id: The ID of the server to stop.
    """
    try:
        server = get_server(server_id)
        server.stop()
    except ServerNotFoundError:
        logger.warning(f"Tried to stop server {server_id}, but it was not found.")

def get_server_status(server_id: int) -> str:
    """Gets the status of a server.

    Args:
        server_id: The ID of the server to get the status of.

    Returns:
        The status of the server.
    """
    try:
        server = get_server(server_id)
        return server.get_status()
    except ServerNotFoundError:
        logger.warning(f"Tried to get status of server {server_id}, but it was not found.")
        return "unknown"
