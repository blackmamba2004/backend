from typing import Any

import yaml
import os


def load_config(env_var: str) -> dict[str, Any]:
    config_path = os.getenv(env_var)
    with open(config_path, "r") as file:
        return yaml.safe_load(file)

def load_main_config():
    return load_config("MAIN_CONFIG_PATH")


def load_logger_config():
    return load_config("LOGGER_CONFIG_PATH")
