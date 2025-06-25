import uuid

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from app.components.types import UserRole
from app.models import BaseModel
from app.models.mixin import TimestampMixin


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
        Enum(UserRole, name="UserRole"),
        default=UserRole.USER,
        nullable=False
    )
