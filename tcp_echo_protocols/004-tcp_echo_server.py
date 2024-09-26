# add protocols:
# ServerConfig, MessageProcessor, ConnectioHandler, ServerLifecycle
import socket
import logging
from protocols import ServerConfig
from implementation import HardcodedConfig


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)


class Server:
    def __init__(self, config: ServerConfig):
        self.host = config.get_host()
        self.port = config.get_port()

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            logger.info(f"Server listening on {self.host}:{self.port}")

            conn, addr = s.accept()
            with conn:
                logger.debug(f"Connected by {addr}")
                data = conn.recv(1024)
                if data:
                    conn.sendall(data)
                logger.info("Server closing after one echo")


if __name__ == "__main__":
    server = Server(config=HardcodedConfig())
    server.run()
