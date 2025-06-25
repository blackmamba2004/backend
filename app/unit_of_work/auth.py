

from app.repository import UserRepository
from app.unit_of_work.base import BaseUnitOfWork


class AuthUnitOfWork(BaseUnitOfWork):
    """
    UnitOfWork для сервиса Auth
    """
    user_repository: UserRepository = None
