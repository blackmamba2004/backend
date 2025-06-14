from enum import Enum, unique


@unique
class UserType(str, Enum):
    USER = 'USER'
    BROKER = 'BROKER'
