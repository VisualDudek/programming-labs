import socket
import logging
from typing import Dict, Union
import signal
import sys


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    encoding='utf-8',
)


class Server():
    def __init__(self, host='127.0.0.1', port=5000, backlog=128):
        self.host: str = host
        self.port: int = port
        self.backlog: int = backlog
        self.server_socket: socket = None

    def run(self):
        # create IPv4(AT_INET) TCP(SOCK_STREAM) socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # log server socket options
        logger.debug(f"--- START Logging server socket option ---")
        for option, value in Server.get_socket_options(self.server_socket).items():
            logger.debug(f"{option}: {value}")
        logger.debug(f"--- END Logging server socket option ---")

        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(self.backlog)
        logger.info(f'Server listening on {self.host}:{self.port}')

        # attach SIGINT callback
        signal.signal(signal.SIGINT, self.shutdown)

        # main server loop for multiple connection handling in sequential manner.
        while True:
            conn, addr = self.server_socket.accept()
            with conn:
                logger.debug(f'Connected by {addr}')

                # handle multiple sequential calls from single client
                while True:
                    data = conn.recv(1024)
                    if data:
                        conn.sendall(data)
                    else: 
                        break


    def shutdown(self, signum, frame) -> None:
        logger.info("Server shoutdown")
        self.server_socket.close()
        sys.exit(0)


    def get_socket_options(sock) -> Dict[str, Union[int, str]]:
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


if __name__ == "__main__":
    tcp_echo = Server(host='127.0.0.1')
    tcp_echo.run()
