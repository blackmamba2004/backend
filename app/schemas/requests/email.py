from pydantic import EmailStr

from app.schemas import BaseSchema


class ChangePasswordRequest(BaseSchema):
    email: EmailStr
