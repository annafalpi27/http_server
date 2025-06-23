import threading

from src.my_http_server import MyHTTPServer

def run_concurrent_server():
    server = MyHTTPServer()
    while True:
        client_socket, addr  = server.accept_client() # single client per thread
        t = threading.Thread(target=server.handle_client, args=(client_socket,addr))
        t.start() 

