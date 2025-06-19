#!/bin/sh
set -e

export MAIN_CONFIG_PATH=config/local.yaml
export LOGGER_CONFIG_PATH=config/logger.yaml

# Run migrations
alembic upgrade head

uvicorn --reload app.main:app --host 0.0.0.0 --port 8088
