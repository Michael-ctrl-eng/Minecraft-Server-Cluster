# Minecraft Server Cluster

## Description

This project implements a scalable Minecraft server network architecture designed for high-traffic environments. It aims to provide a robust and automated solution for managing multiple Minecraft servers, dynamically scaling resources based on player demand. The architecture leverages AWS for infrastructure (though the current implementation does not have full AWS integration), Redis for caching and server management, and BungeeCord for load balancing (future implementation).

**Note:** This project is currently in early development. While basic scaling functionality with Redis is implemented, full AWS integration and BungeeCord load balancing are planned for future development.

## Features

*   **Automated Scaling:** Dynamically scales the number of Minecraft servers up or down based on demand (currently using Redis to track the desired number of servers).
*   **Redis Integration:** Uses Redis for caching and storing server scaling information.
*   **Centralized Server Management:** Provides functions to start, stop, and get the status of servers (currently a basic implementation).
*   **CI/CD Pipeline:** Includes a GitHub Actions workflow for automated testing.
*   **Planned:** Integration with AWS Auto Scaling for dynamic infrastructure provisioning.
*   **Planned:** BungeeCord load balancing to distribute players across multiple servers.

## Dependencies

*   Python 3.10
*   `pytest` (for testing)
*   `redis` (for interacting with Redis)
*   `mock` (for mocking in tests)

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Michael-ctrl-eng/Minecraft-Server-Cluster.git
    cd Minecraft-Server-Cluster
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up a Redis Instance**
    *   You will need a running Redis instance for the project to work.
    *   You can run Redis locally, use a cloud provider's managed Redis service, or run it in a Docker container. For example, using Docker:
        ```bash
        docker run --name my-redis -p 6379:6379 -d redis
        ```
    * Ensure you know your Redis instance's host and port (default is `localhost:6379`).

## Usage

**Environment Variables:**

The project currently uses the following environment variables to configure the Redis connection:

*   `REDIS_HOST`: The hostname or IP address of your Redis instance (default: `localhost`).
*   `REDIS_PORT`: The port number of your Redis instance (default: `6379`).

You can set these environment variables in your shell before running the application or in your GitHub Actions workflow (as you have already done).

**Running Locally (Basic Example):**

While there is no main script to run the full application yet, you can interact with the `scaling.py` and `server_manager.py` modules directly in a Python shell to test the basic functionality:

1. **Start a Python shell:**

    ```bash
    python
    ```

2. **Import the modules and functions:**

    ```python
    from src.cluster_manager.scaling import scale_servers, get_servers_to_scale
    from src.cluster_manager.server_manager import start_server, stop_server, get_server_status
    ```

3. **Experiment with the functions:**

    ```python
    >>> scale_servers(5)  # Scale up by 5 servers
    >>> get_servers_to_scale()
    5
    >>> scale_servers(-2) # Scale down by 2 servers
    >>> get_servers_to_scale()
    3
    >>> start_server(1)  # Start server with ID 1 (basic implementation)
    >>> get_server_status(1) # Check server status (basic implementation)
    >>> stop_server(1)   # Stop server with ID 1 (basic implementation)
    ```

**Note:** The `start_server`, `stop_server`, and `get_server_status` functions currently have very basic placeholder implementations. They don't actually start or stop real Minecraft servers yet.

## Testing

To run the tests, use the following command from the root directory of the project:

```bash
pytest tests/ -v
