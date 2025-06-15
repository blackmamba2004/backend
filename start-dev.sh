#!/bin/bash
set -e

sleep 5
# Run migrations
source "$VENV_PATH/bin/activate" && alembic upgrade head

source "$VENV_PATH/bin/activate" && exec python3.12 -m app.main-dev
