from typing import Any

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import as_declarative


@as_declarative()
class BaseModel:
    id: Any
    __name__: str
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"