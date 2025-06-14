#!bin/sh

python3.12 -m venv .venv
. ./.venv/bin/activate
pip install poetry
poetry config virtualenvs.create false
poetry install --no-root