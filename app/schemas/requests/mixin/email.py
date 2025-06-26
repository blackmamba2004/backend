from pydantic import EmailStr, field_validator

from app.schemas import BaseSchema


class EmailMixin(BaseSchema):
    email: EmailStr

    @field_validator("email", mode="before")
    def email_to_lower(cls, v: str) -> str:
        if isinstance(v, str):
            return v.lower()
        return v
