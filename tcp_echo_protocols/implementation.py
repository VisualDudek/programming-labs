from socket import socket
from protocols import MessageProcessor
import logging

logger = logging.getLogger(__name__)


class EchoProcessor:
    def process_message(self, message: bytes) -> bytes:
        return message


class UpperCaseProcessor:
    def process_message(self, message: bytes) -> bytes:
        return message.upper()


class HardcodedConfig:
    def get_host(self) -> str:
        return "localhost"

    def get_port(self) -> int:
        return 8080


class OneConnectionAtTime:
    def handle_connection(
        self, conn: socket, addr, message_processor: MessageProcessor
    ) -> None:
        with conn:
            logger.debug(f"Connected by {addr}")
            data = conn.recv(1024)
            if data:
                conn.sendall(message_processor.process_message(message=data))
            logger.info("Server closing after one echo")
