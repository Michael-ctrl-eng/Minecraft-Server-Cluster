class ScalingError(Exception):
    """Base class for exceptions in the scaling module."""
    pass

class ServerStartError(Exception):
    """Raised when there is an error starting a server."""
    pass

class ServerStopError(Exception):
    """Raised when there is an error stopping a server."""
    pass

class ServerNotFoundError(Exception):
    """Raised when a server with the given ID is not found."""
    pass

class ConfigError(Exception):
    """Raised when there is an error with the configuration."""
    pass
