from app.schemas import BaseSchema


class TokenPairResponse(BaseSchema):
    access_token: str
    refresh_token: str
    user_role: str
