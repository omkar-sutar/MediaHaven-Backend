#!/bin/bash
source /opt/env.sh
#source ./.venv/Scripts/activate
export PYTHONPATH=$(dirname "$0")

# Restart loop
while true; do
  echo "Starting mediahevenbd"
  python /opt/src/main.py

  # Check the exit status
  if [ $? -ne 0 ]; then
    echo "Python crashed. Restarting..."
    sleep 5  # Delay before restart
  else
    echo "Python exited successfully."
    break
  fi
done
