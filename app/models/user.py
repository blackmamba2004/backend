import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from app.models import BaseModel
from app.models.mixin import TimestampMixin, UserMixin


class User(BaseModel, UserMixin, TimestampMixin):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True, 
        default=uuid.uuid4
    )

    broker_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("brokers.id", onupdate="CASCADE"), 
        index=True
    )
    