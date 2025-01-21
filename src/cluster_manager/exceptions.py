class ScalingError(Exception):
    """Base class for exceptions in the scaling module."""
    pass

class ServerStartError(Exception):
    """Raised when there is an error starting a server."""
    pass

class ServerStopError(Exception):
    """Raised when there is an error stopping a server."""
    pass
