import threading

from src.my_http_server import MyHTTPServer

def run_concurrent_server():
    """
    Starts a concurrent HTTP server that handles each client connection in a separate thread.

    This function creates an instance of `MyHTTPServer` and enters an infinite loop,
    accepting incoming client connections. For each client, it spawns a new thread to
    handle the client using the server's `handle_client` method, allowing multiple clients
    to be served concurrently.

    Note:
        - Each client connection is handled in its own thread.
        - The server runs indefinitely until externally stopped.
    """
    server = MyHTTPServer()
    while True:
        client_socket, addr  = server.accept_client() # single client per thread
        t = threading.Thread(target=server.handle_client, args=(client_socket,addr))
        t.start() 

