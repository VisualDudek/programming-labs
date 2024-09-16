import socket
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    encoding='utf-8',
)


class Server():
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            logger.info(f'Server listening on {self.host}:{self.port}')
            
            conn, addr = s.accept()
            with conn:
                logger.debug(f'Connected by {addr}')

                # handle multiple sequential calls from single client
                while True:
                    data = conn.recv(1024)
                    if data:
                        conn.sendall(data)
                    else: 
                        break

                logger.info("Server shoutdown")


if __name__ == "__main__":
    tcp_echo = Server(host='127.0.0.1')
    tcp_echo.run()
