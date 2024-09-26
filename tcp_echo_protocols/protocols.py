from typing import Protocol
from socket import socket


class ServerConfig(Protocol):
    def get_host(self) -> str: ...

    def get_port(self) -> int: ...


class MessageProcessor(Protocol):
    def process_message(self, message: bytes) -> bytes: ...


class ConnectionHandler(Protocol):
    def handle_connection(
        self, conn: socket, addr, message_processor: MessageProcessor
    ) -> None: ...


class ServerLifecycle(Protocol):
    def start(self) -> None: ...

    def stop(self) -> None: ...
