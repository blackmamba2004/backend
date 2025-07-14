import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.models import BaseModel
from app.models.mixin import TimestampMixin


class BrokerServiceAccount(BaseModel, TimestampMixin):
    __tablename__ = 'broker_service_accounts'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True, 
        default=uuid.uuid4
    )
    broker_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", onupdate="CASCADE"), index=True, nullable=False
    )
    service_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("services.id", onupdate="CASCADE"), index=True, nullable=False
    )

    login: Mapped[str] = mapped_column(index=True, nullable=False)
    password: Mapped[str] = mapped_column(index=True, nullable=False)

    __table_args__ = (
        UniqueConstraint("broker_id", "service_id"),
    )

    broker = relationship("User", back_populates="service_accounts")
