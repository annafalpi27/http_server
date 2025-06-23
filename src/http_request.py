

from typing import Dict, Tuple


class HTTPRequest():
    def __init__(self, request_data: str) -> None:
        """
        Initializes an HTTP request object by parsing the raw HTTP request data.
        Args:
            request_data (str): The raw HTTP request as a string, including the request line, headers, and body.
        """

        request_data = request_data.split("\r\n")
                
        request_line = request_data[0]
        self.method, self.path, self.http_version = request_line.split()

        self.body = request_data.pop()
        
        raw_headers = request_data[1:] 
        raw_headers.pop()  # headers are separated by \r\n and we need to pop it
        self.headers = {item.split(":", 1)[0]: item.split(":", 1)[1].strip() for item in raw_headers}
    
    def parse(self) -> Tuple[str, str, str, Dict, str]:
        """
        Parses the HTTP request and returns its components.

        Returns:
            Tuple[str, str, str, Dict, str]: A tuple containing:
                - method (str): The HTTP method (e.g., 'GET', 'POST').
                - path (str): The requested path.
                - http_version (str): The HTTP version (e.g., 'HTTP/1.1').
                - headers (Dict): A dictionary of HTTP headers.
                - body (str): The body of the HTTP request.
        """
        return self.method, self.path, self.http_version, self.headers, self.body
      