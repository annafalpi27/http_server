


from src.concurrent_server import run_concurrent_server


if __name__ == "__main__":
    """
    We use a general server but a single client per thread.
    recv()  (get response method) break loop or handle exception; no need to manually kill.
    """
    run_concurrent_server()
