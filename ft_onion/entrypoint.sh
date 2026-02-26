#!/bin/bash

echo "[i] Starting container..."

# SSH
service ssh start
status=$?
if [ $status -ne 0 ]; then
    echo "[x] SSH Error: $status"
fi

# Tor
tor &
echo "[i] Tor running in background"

# Nginx
service nginx start
status=$?
if [ $status -ne 0 ]; then
    echo "[x] Nginx Error: $status"
fi

echo "[i] All services started. Waiting..."
tail -f /var/log/nginx/access.log /var/log/nginx/error.log /var/lib/tor/hidden_service/hostname
