from sqlalchemy.orm import Mapped, mapped_column


class UserMixin:
    first_name: Mapped[str] = mapped_column(index=True)
    last_name: Mapped[str] = mapped_column(index=True)
    email: Mapped[str] = mapped_column(index=True, unique=True, nullable=False)
    tel: Mapped[str] = mapped_column(index=True, unique=True, nullable=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=False)
