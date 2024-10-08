import socket

def start_echo_server(host='127.0.0.1', port=5000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f'Server listening on {host}:{port}')
        
        conn, addr = s.accept()
        with conn:
            print(f'Connected by {addr}')
            data = conn.recv(1024)
            if data:
                conn.sendall(data)
            print("Server closing after one echo")

if __name__ == "__main__":
    start_echo_server()
