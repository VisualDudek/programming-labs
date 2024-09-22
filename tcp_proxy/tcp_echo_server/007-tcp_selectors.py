# refactor 006
# add Server calss with accept and read as methods
# why server socket is not AF_INET type?
# why should be ready? what can goes wrong?
# TODO: add KeyboardInterrupt exception handling


import selectors
import socket
import logging
from typing import Optional
from helper import log_socket_optioins, get_socket_options


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    encoding='utf-8',
)
logger = logging.getLogger(__name__)

class Server():
    def __init__(self, host: str ='localhost', port: int = 5000) -> None:
        self.host: str = host
        self.port: int = port
        self.sel: Optional[selectors.DefaultSelector] = None
        self.server_socket: Optional[socket.socket]  = None


    def run(self) -> None:
        self.sel = selectors.DefaultSelector()
        self.server_socket = socket.socket()  # Why not AT_INET and SOCK_STREAM?

        log_socket_optioins(get_socket_options(self.server_socket))
    
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        self.server_socket.setblocking(False)
        self.sel.register(self.server_socket, selectors.EVENT_READ, self.accept)
        logger.info(f"Server listening on {self.host}:{self.port}")

        while True:
            events = self.sel.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)


    def accept(self, sock: socket.socket, mask) -> None:
        '''
        Accept client connection, set nonblocking on ephemeral socket, register file obj
        '''

        conn, addr = sock.accept()  # Should be ready ???
        logger.info(f"accepted {conn} from {addr}")
        conn.setblocking(False)
        self.sel.register(conn, selectors.EVENT_READ, self.read)


    def read(self, conn: socket.socket, mask) -> None:
        '''
        Read data from client and send back echo msg.
        Close client socket if zero bytes recv.
        '''

        data = conn.recv(1000)  # Should be ready
        if data:
            logger.debug(f"echoing {repr(data)} to {conn}")
            conn.send(data)  # Hope it won't block
        else:
            logger.info(f"closing {conn}")
            self.sel.unregister(conn)
            conn.close()


if __name__ == "__main__":
    server = Server(host='localhost', port=5000)
    server.run()