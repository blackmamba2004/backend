

from app.repository import ServiceRepository
from app.unit_of_work.base import BaseUnitOfWork


class ServiceUnitOfWork(BaseUnitOfWork):
    """
    UnitOfWork для сервиса Auth
    """
    service_repository: ServiceRepository = None
