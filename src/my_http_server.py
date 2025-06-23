import socket
import os
from src.http_response import HTTPResponse
from src.http_request import HTTPRequest
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MyHTTPServer")

class MyHTTPServer():
    def __init__(self, host: str = "localhost", port: int = 4221):
        self.server_socket = socket.create_server((host, port), reuse_port=True) 

    def accept_client(self):
        """ Accepts a client connection and initializes the client socket. """
        client_socket, addr = self.server_socket.accept()
        logger.info(f"[+] New connection from {addr}")
        return client_socket, addr # GOOD PRACTICE: Separation of Responsibilities

    def send_response(self, client_socket, status_code:int =200, headers: dict = {}, body: str = ''):
        """
        Sends an HTTP response to the client.
        """
        response = HTTPResponse(status_code=status_code, body=body, request_headers=headers, http_version=self.http_version)
        client_socket.send(response.build())
    
    def manage_get_endpoints(self, client_socket, path, http_version, request_headers):
        """
        Handles GET requests for the server.
        """
        self.http_version = http_version
        match (path):
            case ('/'):
                self.send_response(client_socket=client_socket, body='Welcome to My HTTP Server!', headers=request_headers)

            case (p) if p.startswith('/echo'):
                body = p[6:]  # Strip "/echo"
                self.send_response(client_socket=client_socket, body=body, headers=request_headers)

            case (p) if p.startswith('/user-agent'):
                user_agent = request_headers.get('User-Agent', 'No User-Agent provided')
                self.send_response(client_socket=client_socket, body=user_agent, headers=request_headers)

            case (p) if p.startswith('/files'):
                file_name = os.path.basename(p[7:])
                file_path = os.path.join('files', file_name)
                if os.path.isfile(file_path):
                    with open(file_path, 'r') as f:
                        content = f.read()
                    self.send_response(client_socket=client_socket, body=content, headers=request_headers)
                else:
                    self.send_response(client_socket=client_socket, status_code=404, headers=request_headers)
            case _:
                self.send_response(client_socket=client_socket, status_code=404, headers=request_headers)

    def manage_post_endpoints(self, client_socket, path, http_version, request_headers, request_body):
        """
        Handles POST requests for the server.
        """
        self.http_version = http_version
        match (path):
            case (p) if p.startswith('/files'):
                endpoint_name = p.split("/")[1]
                file_name = path[len(endpoint_name)+1:]
                with open(f"files/{file_name}", 'w') as file:
                    file.write(request_body)
                    self.send_response(client_socket=client_socket, status_code=201, body=request_body, headers=request_headers)
            
            case _:
                self.send_response(client_socket=client_socket, status_code=404, headers=request_headers)
    
    def handle_client(self, client_socket, addr):
        client_socket.settimeout(5) 
        while True:
            try:
                request = client_socket.recv(1024).decode() # bufsize = 1024 bytes
                logger.info(f"[+] Processing request: {request.split('\r\n')[0]} from {addr}")
                
                if not request: # in case we receive an empty request
                    break
                
                method, path, http_version, request_headers, request_body = HTTPRequest(request).parse()
                
                if method == 'GET':
                    self.manage_get_endpoints(client_socket, path, http_version, request_headers)
                elif method == 'POST':
                    self.manage_post_endpoints(client_socket, path, http_version, request_headers, request_body)

                if http_version == 'HTTP/1.0':
                    break
                else:
                    keep_alive = request_headers.get('Connection', '').lower() != 'close'
                    if not keep_alive:  
                        break
            
            except socket.timeout:
                logger.info(f"[-] Connection from {addr} timed out.")
        
        if http_version == 'HTTP/1.0' or not keep_alive:
            client_socket.close()
            logger.info(f"[-] Connection closed from {addr}")