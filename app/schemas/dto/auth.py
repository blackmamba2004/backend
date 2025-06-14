from app.schemas import BaseSchema


class ResetPasswordDTO(BaseSchema):
    email_token: str
    password: str
