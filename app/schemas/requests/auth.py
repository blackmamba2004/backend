from app.schemas import BaseSchema


class ResetPasswordRequest(BaseSchema):
    email_token: str
    password: str

class LogoutRequest(BaseSchema):
    refresh_token: str
