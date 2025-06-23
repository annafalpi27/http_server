


class HTTPRequest():
    def __init__(self, request_data: str) -> None:
        request_data = request_data.split("\r\n")
                
        request_line = request_data[0]
        self.method, self.path, self.http_version = request_line.split()

        self.body = request_data.pop()
        
        raw_headers = request_data[1:] 
        raw_headers.pop()  # headers are separated by \r\n and we need to pop it
        self.headers = {item.split(":", 1)[0]: item.split(":", 1)[1].strip() for item in raw_headers}
    
    def parse(self):
        return self.method, self.path, self.http_version, self.headers, self.body
      