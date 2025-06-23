## How to create an HTTP sever

#### Previous knowledge -  The ` python socket` module

The `socket` module in Python provides a low-level interface for network communication using  **sockets** , which are endpoints for sending and receiving data across a network (TCP/IP or UDP)

#### What is a socket? `server_socket `vs `client_socket`

A **socket** is an endpoint for sending or receiving data across a computer network.

* **`server_socket`** : An endpoint that **binds to a specific address and port and waits for incoming connection** from clients (i.e., like a **shopkeeper** waiting for customers).
* **`client_socket`** : An endpoint that **initiates a connection to a server socket** to communicate (i.e., like a **shop client** entering a store to start interaction).

Both entities create a **client-server architecture.**

#### Request vs Responses:

In a client-server architecture communication happens in a back-and-forth pattern:

* The client sends a **request** to the  server .
* The **server **processes that request and sends back a  **response** .

##### **Communication protocols: HTTP or TPC?**

In the sever-client communication process, 2 different protocols are involved: TCP and HTTP

* **TCP** is a **transport-layer protocol** — it handles reliable connection, delivery, and order of data.
* **HTTP** is an **application-layer protocol** — it defines how clients and servers communicate over the web.

When you open a website:

1. Your browser (client) uses **HTTP** to format a request.
2. That request is sent **over a TCP connection** to the web server.
3. The server responds with an  **HTTP response** , also over TCP.

Some other application-layer protocols that use TCP are:

* **HTTP** – Web browsing (port 80)
* **HTTPS** – Secure web browsing (port 443)
* **FTP** – File transfer (port 21)
* **SMTP** – Sending emails (port 25)
* **SSH** – Secure remote access (port 22)
* **MySQL** – Database communication (port 3306)
* **PostgreSQL** – Database communication (port 5432)

##### **Re**ponse HTTP structure:

A **response** is the message the server sends back to the client after handling the request. It is made up of three parts, each separated by a [CRLF](https://developer.mozilla.org/en-US/docs/Glossary/CRLF) (`\r\n`):

```bash
// Status line
HTTP/1.1  // HTTP version
200       // Status code
OK        // Optional reason phrase
\\r\\n      // CRLF that marks the end of the status line

// Headers: Provide metadata about the response.
blabla
\\r\\n      // CRLF that marks the end of the headers

// Response body (empty)
```

#### Request  HTTP structure:

An HTTP request is made up of three parts, each separated by a [CRLF](https://developer.mozilla.org/en-US/docs/Glossary/CRLF) (`\r\n`):

```bash
// Request line
GET                          // HTTP method
/index.html                  // Request path
HTTP/1.1                     // HTTP version
\\r\\n                         // CRLF that marks the end of the request line

// Headers
Host: localhost:4221\\r\\n     // Header that specifies the server host and port
User-Agent: curl/7.64.1\\r\\n  // Header that describes the client user agent
Accept: */*\\r\\n              // Header that specifies the media types the client can accept
\\r\\n                         // CRLF that marks the end of the headers

// Request body (empty)
```

As we are creatig an HTTP server, our main job is being able to understand HTTP requests (parsing them) and creating HTTP responses.

#### Concurrent server - Managing Multiple Concurrent Connections with `socket`

In an HTTP server, concurrency refers to the server's ability to **handle multiple requests at the same time** or nearly at the same time.

To handle  **multiple concurrent connections** , you typically use one of these approaches:

1. **Multi-threading** – A new thread handles each client. It is the simplest to understand and implement but it is not scalable for many clients
2. **Multi-processing** – A new process handles each client. Also quite simple and better for CPU-heavy tasks.
3. **Async I/O** – Use `asyncio` or non-blocking sockets. Complex but highly scalable
4. **Selectors** – Efficiently manage multiple sockets (recommended for scalability). Advanced level.

##### Client concurrency using Threads

A **thread** is the smallest unit of execution in a process. **It shares the same memory space and resources (variables, files, etc.) with other threads in the same process**, but runs  **independently** .

### **Persistent server -  HTTP keep-alive**

In an HTTP server, p**ersistence** refers to the ability to **keep a connection open** between a client (like a browser) and a server  **after a request is completed** , so that the **same connection can be reused** for multiple requests and responses.

* In HTTP/1.1, connections are  **persistent by default** .
* This means: **one TCP connection is reused** for multiple HTTP requests/responses between a client and a server.

To implement a persistent server it is important to:

* Maintain a read/write loop per client as long as the connection is active and the client does not indicate that it wants to close.
* Read multiple requests from the same socket.
* Close connection only if the client requests it (Connection: close) or if there is an error.

##### ***Persistance Vs Concurrency - key differences***

Concurrency allows handling many clients at once, while persistence allows each client to make many requests without reconnecting each time.

##### *Persistance in HTTP/1.0  vs Persistance in HTTP/1.1*

| Feature                       | HTTP/1.0                                                                           | HTTP/1.1                                                   |
| ----------------------------- | ---------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| **Default connection**  | Non-persistent (close after response)                                              | Persistent (keep connection open by default)               |
| **To keep alive**       | Client must send `Connection: keep-alive` header                                 | Persistent unless `Connection: close` header is sent     |
| **To close connection** | Connection closes after each request unless `keep-alive` requested and supported | Either client or server sends `Connection: close` header |

### HTTP Compression

**HTTP** **compression**is a technique used to **reduce the size of data transferred** between a web server and a client.

An HTTP client uses the `Accept-Encoding` header to specify the compression schemes it supports.

```
> GET /echo/foo HTTP/1.1
> Host: localhost:4221
> User-Agent: curl/7.81.0
> Accept: */*
> Accept-Encoding: gzip  // Client specifies it supports the gzip compression scheme.
```

The server then chooses one of the compression schemes listed in `Accept-Encoding` and compresses the response body with it.
