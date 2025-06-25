#!/bin/sh
set -e

export MAIN_CONFIG_PATH=config/local.yaml
export LOGGER_CONFIG_PATH=config/logger.yaml

# Run migrations
alembic upgrade head

uvicorn --reload app.main:app --host 127.0.0.1 --port 8088
