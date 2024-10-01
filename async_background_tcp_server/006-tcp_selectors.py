# diffrent approach how to handle events in main event loop
# in prevous example callback fn was passed by data in SelectorKey
# here we have different approach to event loop logic
# IMPORTANT: when handling with endless loop -> implement KeyboardInterrupt
# exception handling
# Takeaway: types.SimpleNemespace, disadvantage is lack of type hints for this structure
# ??? how does it work without seting options e.g. sock family for server socket?
# server socket without options -> socket.socket() will not have TIME_WAIT state after closing ?


import logging
import selectors
import socket
import types
import asyncio
from typing import List


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)
logger = logging.getLogger(__name__)
logger.info(
    f"Logger is running in {logging._levelToName[logger.getEffectiveLevel()]} level"
)


class Server:
    def __init__(self, host: str = "localhost", port: int = 5000) -> None:
        self.host: str = host
        self.port: int = port
        self.sel: selectors.DefaultSelector
        self.server_socket: socket.socket
        self.conn_counter: int = 0
        self.tasks: List[asyncio.Task] = []

    async def run(self) -> None:
        self.sel = selectors.DefaultSelector()
        logger.info(f"Selector class in use: {type(self.sel)}")

        self.server_socket = socket.socket()  # Why not AT_INET and SOCK_STREAM?
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        self.server_socket.setblocking(False)

        # here we pass None in data -> This will imply in event loop
        # that this incoming conn
        self.sel.register(self.server_socket, selectors.EVENT_READ, data=None)

        logger.info(f"Server listening on {self.host}:{self.port}")

        # run print task in background
        task = asyncio.create_task(self.print_conn())
        self.tasks.append(task)

        # Server event loop
        try:
            while True:
                await asyncio.sleep(0)  # AAAAAAAAA GOTCHA
                events = self.sel.select(timeout=1)
                for key, mask in events:
                    if key.data is None:
                        # THIS IS CRAZY !!!
                        # Why we can't use key.fileobj here? -> mypy error
                        # sock = socket.fromfd(key.fd, socket.AF_INET, socket.SOCK_STREAM)
                        self.conn_counter += 1
                        self.accept(key.fileobj)  # type: ignore
                    else:
                        self.handle_conn(key, mask)
        except KeyboardInterrupt:
            logger.info("Stopping server ...")
        finally:
            self.sel.close()

    async def print_conn(self):
        print("print_conn started")
        while True:
            print(f"\r{' '*80}\rActive conn. {self.conn_counter}", end="")
            await asyncio.sleep(1)

    def accept(self, sock: socket.socket) -> None:
        """
        Accept client connection, set nonblocking on ephemeral socket, register file obj
        """
        conn, addr = sock.accept()  # Should be ready ???
        logger.debug(f"accepted {conn} from {addr}")
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(conn, events=events, data=data)

    def handle_conn(self, key: selectors.SelectorKey, mask) -> None:
        """ """
        conn: socket.socket = key.fileobj  # type: ignore
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = conn.recv(1024)  # Should be ready
            if recv_data:
                data.outb += recv_data
            else:
                logger.debug(f"closing {conn}")
                self.sel.unregister(conn)
                conn.close()
                self.conn_counter -= 1
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                logger.debug(f"Echoing {data.outb} to {data.addr}")
                sent = conn.send(data.outb)
                data.outb = data.outb[sent:]  # nice self flush-cleanse


if __name__ == "__main__":
    server = Server(host="localhost", port=5000)
    asyncio.run(server.run())
