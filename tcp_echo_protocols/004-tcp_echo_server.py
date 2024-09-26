# add protocols:
# ServerConfig, MessageProcessor, ConnectioHandler, ServerLifecycle
import socket
import logging
from protocols import ServerConfig, ConnectionHandler, MessageProcessor
from implementation import HardcodedConfig, OneConnectionAtTime, UpperCaseProcessor


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)


class Server:
    def __init__(
        self,
        config: ServerConfig,
        conn_handler: ConnectionHandler,
        mess_processor: MessageProcessor,
    ):
        self.host = config.get_host()
        self.port = config.get_port()
        self.conn_handler = conn_handler
        self.mess_processor = mess_processor

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            s.listen()
            logger.info(f"Server listening on {self.host}:{self.port}")

            conn, addr = s.accept()
            self.conn_handler.handle_connection(conn, addr, self.mess_processor)


if __name__ == "__main__":
    server = Server(
        config=HardcodedConfig(),
        conn_handler=OneConnectionAtTime(),
        mess_processor=UpperCaseProcessor(),
    )
    server.run()
