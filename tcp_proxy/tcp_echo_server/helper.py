import logging
import socket
from typing import Dict, Union

logger = logging.getLogger(__name__)


def log_socket_optioins(d: Dict[str, Union[int, str]]) -> None:
    logger.debug("--- START Logging socket option ---")
    for option, value in d.items():
        logger.debug(f"{option}: {value}")
    logger.debug("--- END Logging socket option ---")


def get_socket_options(sock: socket.socket) -> Dict[str, Union[int, str]]:
    # Get all IPv4/TCP socket options
    # e.g.
    # SO_SNDBUF: 16384

    # List of options to check
    socket_options = [
        (socket.SOL_SOCKET, socket.SO_REUSEADDR, "SO_REUSEADDR"),
        (socket.SOL_SOCKET, socket.SO_KEEPALIVE, "SO_KEEPALIVE"),
        (socket.SOL_SOCKET, socket.SO_RCVBUF, "SO_RCVBUF"),
        (socket.SOL_SOCKET, socket.SO_SNDBUF, "SO_SNDBUF"),
        (socket.SOL_SOCKET, socket.SO_LINGER, "SO_LINGER"),
        (socket.SOL_SOCKET, socket.SO_BROADCAST, "SO_BROADCAST"),
        (socket.SOL_SOCKET, socket.SO_TYPE, "SO_TYPE"),
        (socket.IPPROTO_TCP, socket.TCP_NODELAY, "TCP_NODELAY"),
    ]

    results: Dict[str, Union[int, str]]  = {}

    for level, optname, optstr in socket_options:
        try:
            optval = sock.getsockopt(level, optname)
            results[optstr] = optval
        except OSError as e:
            results[optstr] = f"Error: {e}"

    return results