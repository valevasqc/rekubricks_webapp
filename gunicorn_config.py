"""Gunicorn configuration for production deployment."""
import os

# Bind to 0.0.0.0 with PORT from environment
bind = f"0.0.0.0:{os.environ.get('PORT', '10000')}"

# Worker configuration
workers = 2  # For free tier, 2 workers is optimal
worker_class = "sync"
worker_connections = 1000
timeout = 120  # Increase timeout for large Excel file loading
keepalive = 5

# Logging
accesslog = "-"  # Log to stdout
errorlog = "-"   # Log to stderr
loglevel = "info"

# Process naming
proc_name = "rekubricks"

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (Render handles this)
forwarded_allow_ips = "*"
secure_scheme_headers = {
    "X-FORWARDED-PROTOCOL": "ssl",
    "X-FORWARDED-PROTO": "https",
    "X-FORWARDED-SSL": "on",
}
