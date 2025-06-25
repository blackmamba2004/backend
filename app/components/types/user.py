from enum import Enum, unique


@unique
class UserRole(str, Enum):
    USER = 'USER'
    BROKER = 'BROKER'
