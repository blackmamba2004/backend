from app.schemas import BaseSchema


class EmailTokenRequest(BaseSchema):
    email_token: str


class RefreshTokenRequest(BaseSchema):
    refresh_token: str
