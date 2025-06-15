from pathlib import Path


def get_prod_config_path() -> str:
    return Path(__file__).parent / "prod.yaml"

def get_dev_config_path() -> str:
    return Path(__file__).parent / "dev.yaml"

def get_local_config_path() -> str:
    return Path(__file__).parent / "local.yaml"

def get_logger_config_path() -> str:
    return Path(__file__).parent / "logger.yaml"
