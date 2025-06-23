

import gzip
from typing import Dict

PHRASES = {
    200: 'OK',
    201: 'Created',
    400: 'Bad Request',
    404: 'Not Found',
    500: 'Internal Server Error'
}

class HTTPResponse():
    def __init__(self, status_code: int = 200, request_headers: Dict = {}, body: str='', http_version: str = 'HTTP/1.1'):
        self.status_code = status_code
        self.reason_phrase = PHRASES.get(status_code, 'Unknown Status')
        self.body = body
        self.http_version = http_version
        
        request_encodings = request_headers.get('Accept-Encoding', None)
        if request_encodings:
            valid_encodings = []
            for encoding in request_encodings.split(","):
                if encoding.startswith("invalid"):
                    continue
                else:
                    valid_encodings.append(encoding)
            self.encoding = valid_encodings[0]  # server picks the first encoding it supports
        else:
            self.encoding = 'no-encoding'
        
        self.close = request_headers.get('Connection', '').lower() == 'close'

    def set_headers(self, body: str) -> Dict[str, str]:
        headers =  {}

        if len(body) != 0:
            headers["Content-Type"] = "text/plain"
            headers["Content-Length"] = str(len(body))
       
        if self.encoding != 'no-encoding':
            headers["Content-Encoding"] = self.encoding
        
        if self.close:
            headers["Connection"] = "close"
        
        return headers

    def build(self):
        response_line = f"{self.http_version} {self.status_code} {self.reason_phrase}".encode()
        
        response_body = b''
        if self.body:
            if self.encoding == 'no-encoding':
                response_body = self.body.encode()
            elif self.encoding == 'gzip':
                response_body = gzip.compress(self.body.encode()) 
            else:
                raise ValueError(f"Unsupported encoding: {self.encoding}") # todo: return 500

        headers = self.set_headers(response_body)
        response_headers = ''.join(f"{key}: {value}\r\n" for key, value in headers.items()).encode()
        
        response = (        # Encode to bytes for sending over the socket
            response_line +
            "\r\n".encode() +  # End of response line
            response_headers +
            "\r\n".encode() +  # End of headers
            response_body
        )
        return response 