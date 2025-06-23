# MyHTTPServer – Lightweight Concurrent HTTP Server

This repository implements a lightweight, **persistent** and **concurrent** **HTTP server** in Python. It supports **GET** and **POST** requests across multiple custom endpoints.

The server is built using low-level sockets and provides basic HTTP functionality without relying on external web frameworks.

## ⚙️ Architecture

The module is organized into three main classes:

* **`MyHTTPServer`**

  Handles socket creation, listens for incoming client connections, and delegates the processing of HTTP requests. It routes the requests to appropriate handlers and sends structured responses using the other two classes.
* **`HTTPRequest`**

  Parses incoming HTTP requests. It extracts key components such as the HTTP method (`GET`, `POST`), URL path, version, headers, and body content (if present). These parsed values are made available for further logic.  
* **`HTTPResponse`**

  Constructs the HTTP response. It sets the headers based on request origin and capabilities (e.g., `Accept-Encoding`) and compresses the body using **gzip** if the client supports it.

For more details about the HTTP request and response structure, refer to `docs/HTTP_SERVER.md`.

The server's concurrency is managed by the `run_concurrent_server` function. Under the hood, each connection is handled independently using Python's `threading` module, enabling the server to process simultaneous HTTP requests without blocking.

### 📌 Supported Endpoints

| Method | Endpoint            | Description                                                                 |
| ------ | ------------------- | --------------------------------------------------------------------------- |
| GET    | `/`               | Returns a welcome message.                                                  |
| GET    | `/echo/<message>` | Returns the text `<message>`back to the client.                           |
| GET    | `/user-agent`     | Returns the value of the client's `User-Agent`header.                     |
| GET    | `/files/<name>`   | Returns the contents of the file `<name>`located in the `files/`folder. |
| POST   | `/files/<name>`   | Saves the request body to a file named `<name>`in the `files/`folder.   |

> `404 Not Found` is returned for any unsupported path.

### 🧪 Example Usage

***Start server***

```bash
source venv/bin/activate
python main.py
```

***Make requests***

```bash
# Root welcome endpoint
curl http://localhost:4221/

# Echo endpoint
curl http://localhost:4221/echo/hello-world

# User-Agent endpoint
curl -H "User-Agent: CustomClient/1.0" http://localhost:4221/user-agent

# Get the contents of an existing file
curl http://localhost:4221/files/foo

# Upload a file using POST
curl -X POST --data "This is file content" http://localhost:4221/files/file_123

# Invalid endpoint
 curl http://localhost:4221/patata
```


### ✅ Testing

This project includes a test suite to verify the correctness of the HTTP server's behavior.

You can run the tests using:

```
make test
```

This command will:

1. Start the server (usually in the background).
2. Run a series of automated tests (e.g., via `pytest` or a custom script).
3. Validate the server's response codes, headers, and body content for supported endpoints.
