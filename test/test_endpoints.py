import logging
import subprocess
import time
import unittest
import threading

from src.concurrent_server import run_concurrent_server

logging.disable(logging.CRITICAL)

SERVER_URL = "http://localhost:4221"
CURL_1_1_TESTS = [
    {
        "command": ["curl", "-i", "-H", "Connection: close", SERVER_URL],
        "expected_response": "HTTP/1.1 200 OK\nContent-Type: text/plain\nContent-Length: 26\nConnection: close\n\nWelcome to My HTTP Server!"
    },
    {
        "command": ["curl", "-i", "-H", "Connection: close", f"{SERVER_URL}/abcdefg"],
        "expected_response": "HTTP/1.1 404 Not Found\nConnection: close\n\n"
    },
    {
        "command": ["curl", "-i", "-H", "Connection: close", f"{SERVER_URL}/echo/abc"],
        "expected_response": "HTTP/1.1 200 OK\nContent-Type: text/plain\nContent-Length: 3\nConnection: close\n\nabc"
    },
    {
        "command": ["curl", "-i", "--header", "User-Agent: foobar/1.2.3", "-H", "Connection: close", f"{SERVER_URL}/user-agent"],
        "expected_response": "HTTP/1.1 200 OK\nContent-Type: text/plain\nContent-Length: 12\nConnection: close\n\nfoobar/1.2.3"
    },
    {
        "command": ["curl", "-i", "-H", "Connection: close", f"{SERVER_URL}/files/foo"],
        "expected_response": "HTTP/1.1 200 OK\nContent-Type: text/plain\nContent-Length: 13\nConnection: close\n\nHello, World!"
    },
    {
        "command": ["curl", "-i", "-H", "Connection: close", f"{SERVER_URL}/files/non_existant_file"],
        "expected_response": "HTTP/1.1 404 Not Found\nConnection: close\n\n"
    },
    {
        "command": ["curl", "-i", "--data", "12345", "-H", "Connection: close", f"{SERVER_URL}/files/file_123"],
        "expected_response": "HTTP/1.1 201 Created\nContent-Type: text/plain\nContent-Length: 5\nConnection: close\n\n12345"
    },
    {   
        "command": ["curl", "-i", "-H", "Accept-Encoding: gzip", "-H", "Connection: close", f"{SERVER_URL}/echo/abc"],
        "expected_response": b'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 23\r\nContent-Encoding: gzip\r\nConnection: close',
        "raw_response": True
    },
    {   
        "command": ["curl", "-i", "-H", "Accept-Encoding: gzip", "-H", "Connection: close", f"{SERVER_URL}/echo/abc"],
        "expected_response": b'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 23\r\nContent-Encoding: gzip\r\nConnection: close',
        "raw_response": True
    },

]

CURL_1_0_TESTS = [
    {
        "command": ["curl", "-i", "--http1.0", SERVER_URL],
        "expected_response": "HTTP/1.0 200 OK\nContent-Type: text/plain\nContent-Length: 26\n\nWelcome to My HTTP Server!"
    }
   
]

PERSISTENT_CONNECTION_TESTS = [
    {
        "command": [
            "curl", "--http1.1", "-i", 
            "http://localhost:4221/echo/orange", 
            "--next", "http://localhost:4221/"
        ],
        # response not representative but reflex multiple requests at same socket
        'expected_response': "HTTP/1.1 200 OK\nContent-Type: text/plain\nContent-Length: 6\n\norangeWelcome to My HTTP Server!",

    }
]

class ServerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        server_thread = threading.Thread(target=run_concurrent_server, daemon=True)
        server_thread.start()
        time.sleep(1)

    def test_curl_1_1_requests(self):
        for  test in CURL_1_1_TESTS:
            raw = test.get("raw_response", False)
            print(f"Running command: {' '.join(test['command'])}")
            result = subprocess.run(test["command"], capture_output=True, text=not raw)
            output = result.stdout
            if raw:
                output = output.split(b'\r\n\r\n')[0]
            expect = test["expected_response"]
            assert output == expect

    def test_curl_1_0_requests(self):
        """Test no-persistent HTTP1.0 connections"""
        for  test in CURL_1_0_TESTS:
            print(f"Running command: {' '.join(test['command'])}")
            result = subprocess.run(test["command"], capture_output=True, text=True)
            output = result.stdout
            expect = test["expected_response"]
            assert output == expect

    def test_persistent_connections(self):
        """Test persistent connections"""
        for  test in PERSISTENT_CONNECTION_TESTS:
            print(f"Running command: {' '.join(test['command'])}")
            result = subprocess.run(test["command"], capture_output=True, text=True)
            output = result.stdout
            expect = test["expected_response"]
            assert output == expect


if __name__ == "__main__":
    unittest.main()