import yaml

from path import get_dev_config_path


def read_config() -> dict[str, dict[str, str | int | bool]]:
    """
    Для чтения конфигов .yaml
    """
    with open(get_dev_config_path(), "r") as file:
        return yaml.safe_load(file)
