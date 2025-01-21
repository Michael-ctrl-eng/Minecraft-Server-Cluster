import yaml
import os
from pydantic import BaseModel, ValidationError, validator

class RedisConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379
    db: int = 0

class ScalingConfig(BaseModel):
    max_servers: int = 10
    min_servers: int = 0

class LoggingConfig(BaseModel):
    level: str = "INFO"
    format: str = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    file: str = None

class AWSConfig(BaseModel):
    region: str = None
    access_key_id: str = None
    secret_access_key: str = None

    @validator("access_key_id", "secret_access_key", always=True)
    def check_aws_credentials(cls, v, values, **kwargs):
        if values.get("region") and not v:
            raise ValueError("AWS access key ID and secret access key are required when region is set")
        return v

class AppConfig(BaseModel):
    redis: RedisConfig = RedisConfig()
    scaling: ScalingConfig = ScalingConfig()
    logging: LoggingConfig = LoggingConfig()
    aws: AWSConfig = AWSConfig()

def load_config(config_file: str = "config.yaml") -> AppConfig:
    """Loads the application configuration from a YAML file and environment variables."""
    try:
        with open(config_file, "r") as f:
            config_data = yaml.safe_load(f)
    except FileNotFoundError:
        config_data = {}

    # Override with environment variables
    for key, value in config_data.items():
        if isinstance(value, dict):
            for subkey, subvalue in value.items():
                env_var = os.environ.get(f"{key.upper()}_{subkey.upper()}")
                if env_var:
                    config_data[key][subkey] = env_var
        else:
            env_var = os.environ.get(key.upper())
            if env_var:
                config_data[key] = env_var

    try:
        config = AppConfig(**config_data)
    except ValidationError as e:
        print(f"Error validating config: {e}")
        raise

    return config
