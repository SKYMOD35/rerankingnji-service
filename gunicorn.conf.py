import multiprocessing
import os

# Determine the number of CPU cores
cpu_cores = multiprocessing.cpu_count()

# Lower worker count to prevent resource exhaustion
workers = int(os.getenv("WORKERS", cpu_cores))  # Use one worker per core

# Type of worker class - 'sync' for simple request handling
worker_class = 'sync'

# Address and port to bind
bind = os.getenv("BIND", "0.0.0.0:5000")

# Timeout in seconds for each worker (handles long-running requests)
timeout = int(os.getenv("TIMEOUT", 60))

# Number of simultaneous clients a worker can handle
worker_connections = int(os.getenv("WORKER_CONNECTIONS", 200))  # Reduced to prevent overload

# Log level (debug, info, warning, error, critical)
loglevel = os.getenv("LOGLEVEL", "info")

# Access log file location (use '-' for standard output)
accesslog = os.getenv("ACCESS_LOG", "-")

# Error log file location (use '-' for standard output)
errorlog = os.getenv("ERROR_LOG", "-")

# Graceful worker timeout handling
graceful_timeout = int(os.getenv("GRACEFUL_TIMEOUT", 60))

# Maximum number of requests a worker will handle before restarting (prevents memory leaks)
max_requests = int(os.getenv("MAX_REQUESTS", 500))
max_requests_jitter = int(os.getenv("MAX_REQUESTS_JITTER", 50))

# Optional: enable keep-alive connections
keepalive = int(os.getenv("KEEPALIVE", 5))
