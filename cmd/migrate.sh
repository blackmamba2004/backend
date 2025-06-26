#!/bin/bash

export MAIN_CONFIG_PATH=config/local.yaml

source .venv/bin/activate

alembic upgrade head