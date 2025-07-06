import uuid
from typing import NewType
from enum import Enum, unique

from sqlalchemy import Enum as PgEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from app.models import BaseModel
from app.models.mixin import TimestampMixin


@unique
class UserRole(str, Enum):
    USER = 'USER'
    BROKER = 'BROKER'
    ADMIN = 'ADMIN'


class User(BaseModel, TimestampMixin):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True, 
        default=uuid.uuid4
    )
    ref_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", onupdate="CASCADE"), index=True, nullable=True
    )

    first_name: Mapped[str] = mapped_column(index=True, nullable=True)
    last_name: Mapped[str] = mapped_column(index=True, nullable=True)
    email: Mapped[str] = mapped_column(index=True, unique=True, nullable=False)
    tel: Mapped[str] = mapped_column(index=True, unique=True, nullable=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=False)
    role: Mapped[UserRole] = mapped_column(
        PgEnum(UserRole, name="UserRole"),
        default=UserRole.USER,
        nullable=False
    )

Admin = NewType('Admin', User)
Broker = NewType('Broker', User)
Client = NewType('Client', User)
AnyUser = NewType('AnyUser', User)