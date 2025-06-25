export MAIN_CONFIG_PATH=config/local.yaml

alembic revision --autogenerate -m "$*"