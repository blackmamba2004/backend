

from app.repository import BrokerRepository, UserRepository
from app.unit_of_work.base import BaseUnitOfWork


class AuthUnitOfWork(BaseUnitOfWork):
    """
    UnitOfWork для сервиса Auth
    """
    broker_repository: BrokerRepository = None
    user_repository: UserRepository = None
