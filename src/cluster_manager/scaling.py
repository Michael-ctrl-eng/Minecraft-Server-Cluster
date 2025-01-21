import logging
import redis
from src.cluster_manager.exceptions import ScalingError

r = redis.Redis(host="localhost", port=6379, db=0)  # You'll manage this with config later

# Define some constants (consider moving these to a config file)
MAX_SERVERS = 10
MIN_SERVERS = 0

def scale_servers(num_servers: int):
    """Scales the number of Minecraft servers up or down.

    Args:
        num_servers: The number of servers to add (positive) or remove (negative).

    Raises:
        TypeError: If num_servers is not an integer.
        ScalingError: If there is an error scaling the servers.
    """
    if not isinstance(num_servers, int):
        raise TypeError("num_servers must be an integer")

    if num_servers > 0:
        if get_servers_to_scale() + num_servers > MAX_SERVERS:
            raise ScalingError("Cannot scale above maximum server limit")
        try:
            r.incr("servers", num_servers)
        except redis.exceptions.TimeoutError as e:
            logging.error(f"Timeout connecting to Redis: {e}")
            raise ScalingError("Failed to scale servers due to Redis timeout") from e
        except redis.exceptions.ConnectionError as e:
            logging.error(f"Error connecting to Redis: {e}")
            raise ScalingError("Failed to scale servers due to Redis connection error") from e
    elif num_servers < 0:
        if get_servers_to_scale() + num_servers < MIN_SERVERS:
            raise ScalingError("Cannot scale below minimum server limit")
        try:
            r.decr("servers", abs(num_servers))
        except redis.exceptions.TimeoutError as e:
            logging.error(f"Timeout connecting to Redis: {e}")
            raise ScalingError("Failed to scale servers due to Redis timeout") from e
        except redis.exceptions.ConnectionError as e:
            logging.error(f"Error connecting to Redis: {e}")
            raise ScalingError("Failed to scale servers due to Redis connection error") from e

def get_servers_to_scale() -> int:
    """Gets the current number of servers to scale from Redis.

    Returns:
        The number of servers to scale.

    Raises:
        ScalingError: If there is an error retrieving the value from Redis.
        ValueError: If the value retrieved from Redis is not a valid integer.
    """
    try:
        servers = r.get("servers")
        if servers is None:
            return 0  # Default to 0 if no value is set
        return int(servers)
    except redis.exceptions.TimeoutError as e:
        logging.error(f"Timeout connecting to Redis: {e}")
        raise ScalingError(
            "Failed to get server count due to Redis timeout"
        ) from e
    except redis.exceptions.ConnectionError as e:
        logging.error(f"Error connecting to Redis: {e}")
        raise ScalingError(
            "Failed to get server count due to Redis connection error"
        ) from e
    except ValueError:
        logging.error(f"Non-integer value retrieved from Redis: {servers}")
        raise ValueError("Invalid server count retrieved from Redis")
