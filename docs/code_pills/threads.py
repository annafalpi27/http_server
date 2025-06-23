import time
import threading




def worker(n):
    print(f"Worker {n} starting")
    time.sleep(2)
    print(f"Worker {n} done")

if __name__ == "__main__":

    """
    How this will work?
        - We will start 1 process (the Python interpreter).
        - The process will start 5 threads.
        - Each thread will run the worker function.
        - The main thread will wait for all threads to finish before exiting.

        [Process]
        ├── [Main Thread]   <- This runs the main script
        ├── [Thread 1]      <- Runs worker(0)
        ├── [Thread 2]      <- Runs worker(1)
        ├── [Thread 3]      <- Runs worker(2)
        ├── [Thread 4]      <- Runs worker(3)
        └── [Thread 5]      <- Runs worker(4)
    """
    
    threads = []
    for i in range(5):
        t = threading.Thread(target=worker, args=(i,))
        t.start()   # Start thread 
        threads.append(t)

    for t in threads:
        t.join() #  tells the main thread to wait until t finishes.