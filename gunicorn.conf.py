import multiprocessing
import os

# Dynamic worker calculation based on CPU cores
cpu_cores = multiprocessing.cpu_count()
workers = min(int(os.getenv("WORKERS", 2 * cpu_cores + 1)), 8)  # Cap at 8 workers max

# Worker type: sync for simplicity, gevent or uvicorn for async support
worker_class = "sync"

# Bind address and port
bind = os.getenv("BIND", "0.0.0.0:5000")

# Timeout settings
timeout = int(os.getenv("TIMEOUT", 120))  # Seconds
graceful_timeout = int(os.getenv("GRACEFUL_TIMEOUT", 30))  # Seconds

# Maximum requests before restarting a worker (prevents memory leaks)
max_requests = int(os.getenv("MAX_REQUESTS", 1000))
max_requests_jitter = int(os.getenv("MAX_REQUESTS_JITTER", 50))  # Add randomness to restarts

# Logging settings
loglevel = os.getenv("LOGLEVEL", "info")
accesslog = os.getenv("ACCESS_LOG", "-")  # "-" means stdout
errorlog = os.getenv("ERROR_LOG", "-")  # "-" means stdout

# Keep-alive settings
keepalive = int(os.getenv("KEEPALIVE", 2))  # Seconds

# Connection settings
worker_connections = int(os.getenv("WORKER_CONNECTIONS", 1000))  # For async workers
