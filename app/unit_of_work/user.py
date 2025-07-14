from app.repository import UserRepository
from app.unit_of_work.base import BaseUnitOfWork


class UserUnitOfWork(BaseUnitOfWork):
    """
    UnitOfWork для управления сервисами(сторонними сущностями)
    """
    user_repository: UserRepository = None
