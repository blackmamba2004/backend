from app.repository import AccountRepository, UserPermissionRepository
from app.unit_of_work.base import BaseUnitOfWork


class AccountUnitOfWork(BaseUnitOfWork):
    """
    UnitOfWork для сервиса управления аккаунтами брокеров
    """
    account_repository: AccountRepository = None
    user_permission_repository: UserPermissionRepository = None
