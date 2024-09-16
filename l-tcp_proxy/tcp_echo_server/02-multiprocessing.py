# This code is so wrong that it's not even funny. It's a good example of how not to use multiprocessing.

import socket
import multiprocessing
from functools import partial

def handle_client(conn):
    """Handle individual client connection."""
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        conn.close()

def worker(conn):
    """Worker function to handle client connections."""
    handle_client(conn)

def server(host='127.0.0.1', port=65432):
    """Main server function."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)
    print(f"Server listening on {host}:{port}")

    # pool = multiprocessing.Pool(processes=5)  # Create a pool of 5 workers
    with multiprocessing.Pool() as pool:

        while True:
            try:
                conn, addr = sock.accept()
                print(f"Accepted connection from {addr}")
                
                # Send the connection to all workers in the pool
                pool.apply_async(worker, (conn,))
                
                # Close the connection immediately
                # conn.close()  # BUG: This will close the connection before the worker can handle it
            except Exception as e:
                print(f"Error accepting connection: {e}")

    sock.close()

if __name__ == "__main__":
    server()
