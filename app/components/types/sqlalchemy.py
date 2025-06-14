from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

AsyncSessionFactory = async_sessionmaker[AsyncSession]


class NullColumn:
    """
    Класс для замены None при явной передаче значения null с API в DTO.
    Предназначен для адекватной передачи установки значений None при обновлении записей в репозитории SQLAlchemy.
    """
    pass