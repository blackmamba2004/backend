#!/bin/bash
set -e

export MAIN_CONFIG_PATH=config/local.yaml
export LOGGER_CONFIG_PATH=config/logger.yaml

source .venv/bin/activate

# Run migrations
alembic upgrade head

uvicorn app.main:app --host 127.0.0.1 --port 8088 --reload --loop uvloop
