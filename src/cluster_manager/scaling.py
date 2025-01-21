import logging
import redis
from pydantic import BaseModel, validator, ValidationError
from src.cluster_manager.config import load_config
from src.cluster_manager.exceptions import ScalingError

config = load_config()
r = redis.Redis(
    host=config.redis.host, port=config.redis.port, db=config.redis.db
)

logger = logging.getLogger(__name__)

class ScaleRequest(BaseModel):
    num_servers: int

    @validator("num_servers")
    def check_scaling_limits(cls, v):
        if v > 0 and v > config.scaling.max_servers:
            raise ValueError("Cannot scale above maximum server limit")
        if v < 0 and abs(v) > get_servers_to_scale():
            raise ValueError("Cannot scale below minimum server limit")
        return v

def scale_servers(num_servers: int):
    """Scales the number of Minecraft servers up or down.

    Args:
        num_servers: The number of servers to add (remove if negative).

    Raises:
        ScalingError: If there is an error scaling the servers.
        TypeError: If num_servers is not an integer.
        ValueError: If scaling request exceeds the limits.
    """
    try:
        scale_request = ScaleRequest(num_servers=num_servers)
    except ValidationError as e:
        logger.error(f"Invalid scaling request: {e}")
        raise ScalingError("Invalid scaling request")

    try:
        if scale_request.num_servers > 0:
            r.incr("servers", scale_request.num_servers)
            logger.info(f"Scaled up by {scale_request.num_servers} servers")
        elif scale_request.num_servers < 0:
            r.decr("servers", abs(scale_request.num_servers))
            logger.info(f"Scaled down by {abs(scale_request.num_servers)} servers")
    except redis.exceptions.TimeoutError as e:
        logger.error(f"Timeout connecting to Redis: {e}")
        raise ScalingError("Failed to scale servers due to Redis timeout") from e
    except redis.exceptions.ConnectionError as e:
        logger.error(f"Error connecting to Redis: {e}")
        raise ScalingError("Failed to scale servers due to Redis connection error") from e
    except Exception as e:
        logger.error(f"An unexpected error occurred during scaling: {e}")
        raise ScalingError("Failed to scale servers") from e

def get_servers_to_scale() -> int:
    """Gets the current number of servers to scale from Redis.

    Returns:
        The number of servers to scale.

    Raises:
        ScalingError: If there is an error retrieving the value from Redis.
    """
    try:
        servers = r.get("servers")
        if servers is None:
            logger.info("No server count found in Redis. Defaulting to 0.")
            return 0
        return int(servers)
    except redis.exceptions.TimeoutError as e:
        logger.error(f"Timeout connecting to Redis: {e}")
        raise ScalingError("Failed to get server count due to Redis timeout") from e
    except redis.exceptions.ConnectionError as e:
        logger.error(f"Error connecting to Redis: {e}")
        raise ScalingError("Failed to get server count due to Redis connection error") from e
    except ValueError:
        logger.error(f"Non-integer value retrieved from Redis: {servers}")
        raise ScalingError("Invalid server count retrieved from Redis")
