#!/bin/bash
source env.sh
source ./.venv/Scripts/activate

export PYTHONPATH=$(dirname "$0")
python ./src/main.py