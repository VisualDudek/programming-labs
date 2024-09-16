import socket

def start_proxy(local_host, local_port, remote_host, remote_port):
    # Create a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Bind the server socket to the local host and port
        server_socket.bind((local_host, local_port))
        
        # Listen for incoming connections
        server_socket.listen(1)
        print(f"Proxy listening on {local_host}:{local_port}")
        
        # Accept an incoming connection
        client_socket, address = server_socket.accept()
        print(f"Connection accepted from {address}")
        
        # Connect to the remote server
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((remote_host, remote_port))
        print(f"Connected to remote server {remote_host}:{remote_port}")
        
        # Proxy loop
        while True:
            # Read from client and send to remote server
            data = client_socket.recv(4096)
            print(f"Received from client: {data.decode('utf-8')}")
            if not data:
                break
            remote_socket.sendall(data)
            
            # Read from remote server and send to client
            data = remote_socket.recv(4096)
            if not data:
                break
            client_socket.sendall(data)
        
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # Close all sockets
        if 'client_socket' in locals():
            client_socket.close()
        if 'remote_socket' in locals():
            remote_socket.close()
        server_socket.close()
        print("Proxy stopped")

if __name__ == "__main__":
    LOCAL_HOST = "localhost"
    LOCAL_PORT = 8000
    REMOTE_HOST = "localhost"
    REMOTE_PORT = 5000
    
    start_proxy(LOCAL_HOST, LOCAL_PORT, REMOTE_HOST, REMOTE_PORT)
