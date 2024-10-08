# add protocols:
# ServerConfig, MessageProcessor, ConnectioHandler, ServerLifecycle
import socket
import logging
from typing import Protocol


class ServerConfig(Protocol):
    def get_host(self) -> str: ...

    def get_port(self) -> int: ...


class MessageProcessor(Protocol):
    def process_message(self, message: bytes) -> bytes: ...


class ConnectionHandler(Protocol):
    def handle_connection(
        self, conn: socket.socket, addr, message_processor: MessageProcessor
    ) -> None: ...


class ServerLifecycle(Protocol):
    def start(self) -> None: ...

    def stop(self) -> None: ...


class EchoProcessor:
    def process_message(self, message: bytes) -> bytes:
        return message


class UpperCaseProcessor:
    def process_message(self, message: bytes) -> bytes:
        return message.upper()


class HardcodedConfig:
    def get_host(self) -> str:
        return "loclahost"

    def get_port(self) -> int:
        return 8080


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
