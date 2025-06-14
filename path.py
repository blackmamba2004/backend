from pathlib import Path


def get_config_path() -> str:
    return Path(__file__).parent / "config.yaml"

def get_logger_config_path() -> str:
    return Path(__file__).parent / "logger.yaml"
