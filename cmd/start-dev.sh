#!/bin/bash
set -e

sleep 3

export MAIN_CONFIG_PATH=config/dev.yaml
export LOGGER_CONFIG_PATH=config/logger.yaml

# Run migrations
source "$VENV_PATH/bin/activate" && (
    alembic upgrade head &&
    uvicorn app.main:app --host 0.0.0.0 --port 8088 --reload
)
