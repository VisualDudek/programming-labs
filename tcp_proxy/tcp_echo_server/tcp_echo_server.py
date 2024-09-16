# tcp_echo_server.py

import socket
import threading
import sys
import signal
from time import sleep
import os

class TCPEchoServer:
    def __init__(self, host='0.0.0.0', port=5000, max_threads=10):
        self.host = host
        self.port = port
        self.server_socket = None
        self.client_sockets = []
        self.semaphore = threading.Semaphore(max_threads)

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(128)
        
        print(f"TCP Echo Server started on {self.host}:{self.port}")

        signal.signal(signal.SIGINT, self.shutdown)

        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"New connection from {addr}")
            self.client_sockets.append(client_socket)
            
            self.semaphore.acquire()
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

    def handle_client(self, client_socket):
        try:
            while True:
                # message = client_socket.recv(4096).decode('utf-8')
                message = client_socket.recv(16).decode('utf-8')
                if not message:
                    print("Connection closed by client")
                    break
                
                upper_case_message = message.upper()
                client_socket.sendall(upper_case_message.encode('utf-8'))
                
                print(f"Echoed: {upper_case_message}")
                print(f"Active threads: {threading.active_count()}")
        finally:
            client_socket.close()
            self.client_sockets.remove(client_socket)
            self.semaphore.release()

    def shutdown(self, signum, frame):
        print("Shutting down server")
        for client_socket in self.client_sockets:
            client_socket.close()
        if self.server_socket:
            self.server_socket.close()
        sys.exit(0)

if __name__ == "__main__":

    current_pid = os.getpid()
    print(f"The current process ID is: {current_pid}")

    server = TCPEchoServer()
    server.start()
