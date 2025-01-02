#!/bin/bash
export PYTHONPATH=$(dirname "$0")

# Restart loop
while true; do
  echo "Starting mediahevenbd"
#  python /opt/src/main.py
  gunicorn -c /opt/gunicorn.conf.py src.main:app
  # Check the exit status
  if [ $? -ne 0 ]; then
    echo "Server crashed. Restarting..."
    sleep 5  # Delay before restart
  else
    echo "Server exited successfully."
    break
  fi
done
