import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from app.models import BaseModel
from app.models.mixin import TimestampMixin


class UserPermission(BaseModel, TimestampMixin):
    __tablename__ = 'user_permissions'

    __table_args__ = (
        UniqueConstraint("broker_account_id", "user_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4
    )
    broker_account_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("broker_service_accounts.id", onupdate="CASCADE", ondelete="CASCADE"), index=True, nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", onupdate="CASCADE"), index=True, nullable=False
    )
    can_trade: Mapped[bool] = mapped_column(default=False, nullable=False)
