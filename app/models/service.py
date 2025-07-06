import uuid

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from app.models import BaseModel
from app.models.mixin import TimestampMixin


class Service(BaseModel, TimestampMixin):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True, 
        default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(index=True, unique=True, nullable=False)
