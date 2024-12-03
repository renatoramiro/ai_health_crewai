# Gunicorn configuration file
import multiprocessing

# Server socket
bind = "0.0.0.0:5005"
backlog = 2048

# Worker processes - minimum configuration
workers = 1  # Single worker to minimize memory usage
worker_class = 'sync'
worker_connections = 10
timeout = 120  # Increased timeout for API responses
keepalive = 2

# Preload application to share memory
preload_app = True

# Restart workers after N requests to prevent memory leaks
max_requests = 50
max_requests_jitter = 10

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'debug'  # Increased logging level for debugging

# Process naming
proc_name = 'gunicorn_flask_app'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# Memory management
worker_tmp_dir = "/dev/shm"  # Use RAM-based tmp directory
threads = 1  # Single thread per worker

# Graceful timeout
graceful_timeout = 30

# SSL
keyfile = None
certfile = None
