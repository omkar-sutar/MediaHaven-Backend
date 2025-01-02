# Number of worker processes
import os
workers = 4  # Adjust based on CPU cores and workload

# Worker class (sync, async, etc.)
worker_class = "sync"

# Timeout for requests (in seconds)
timeout = 120

# The IP address and port to bind
bind = f"0.0.0.0:{os.getenv('SELF_PORT',5001)}"

# Enable access log
accesslog = "-"

# Enable error log
errorlog = "-"

# Log level (debug, info, warning, error, critical)
loglevel = "info"

# Maximum number of pending connections
backlog = 2048

# Whether to preload the application before forking workers
preload_app = True

# Number of threads per worker (useful for I/O-bound tasks)
threads = 2

# Security: limit the size of HTTP request headers
limit_request_fields = 100
limit_request_field_size = 8190  # bytes

# Graceful timeout for shutting down workers
graceful_timeout = 30
