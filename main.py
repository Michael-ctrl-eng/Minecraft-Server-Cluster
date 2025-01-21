import argparse
import logging

from src.cluster_manager.config import load_config, AppConfig
from src.cluster_manager.scaling import scale_servers, get_servers_to_scale
from src.cluster_manager.server_manager import (
    start_server,
    stop_server,
    get_server_status,
)
from src.cluster_manager.exceptions import (
    ScalingError,
    ServerStartError,
    ServerStopError,
    ServerNotFoundError,
)

config = load_config()

def main():
    logging.basicConfig(
        level=config.logging.level,
        format=config.logging.format,
        filename=config.logging.file,  # Optional: Log to file
    )

    parser = argparse.ArgumentParser(description="Minecraft Server Cluster Manager")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Scale command
    scale_parser = subparsers.add_parser("scale", help="Scale servers")
    scale_parser.add_argument(
        "num_servers", type=int, help="Number of servers to add or remove"
    )

    # Status command
    status_parser = subparsers.add_parser("status", help="Get server status")

    # Start command
    start_parser = subparsers.add_parser("start", help="Start a server")
    start_parser.add_argument("server_id", type=int, help="Server ID to start")

    # Stop command
    stop_parser = subparsers.add_parser("stop", help="Stop a server")
    stop_parser.add_argument("server_id", type=int, help="Server ID to stop")

    args = parser.parse_args()

    if args.command == "scale":
        try:
            scale_servers(args.num_servers)
            logging.info(f"Scaled servers by {args.num_servers}")
        except ScalingError as e:
            logging.error(f"Error scaling servers: {e}")
    elif args.command == "status":
        try:
            num_servers = get_servers_to_scale()
            print(f"Number of servers to scale: {num_servers}")
        except ScalingError as e:
            logging.error(f"Error getting server status: {e}")
    elif args.command == "start":
        try:
            start_server(args.server_id)
            logging.info(f"Started server: {args.server_id}")
        except ServerStartError as e:
            logging.error(f"Error starting server: {e}")
    elif args.command == "stop":
        try:
            stop_server(args.server_id)
            logging.info(f"Stopped server: {args.server_id}")
        except ServerStopError as e:
            logging.error(f"Error stopping server: {e}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
