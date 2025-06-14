import re


def camel_to_snake(name: str) -> str:
    """
    Привести строку из CamelCase в snake_case
    :param name: Строка
    :return:
    """
    name_snake = re.sub(r'(?<!^)(?=[A-Z])', '_', name)
    return name_snake.lower()
