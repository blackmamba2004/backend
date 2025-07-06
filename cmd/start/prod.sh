#!/bin/bash
set -e

sleep 3

export MAIN_CONFIG_PATH=config/prod.yaml
export LOGGER_CONFIG_PATH=config/logger.yaml

# Run migrations
source "$VENV_PATH/bin/activate" && (
    alembic upgrade head &&
    gunicorn app.main:app -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:8088
)
