#!/bin/bash
source env.sh

export PYTHONPATH=$(dirname "$0")
python ./src/main.py