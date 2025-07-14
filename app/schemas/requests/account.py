from app.schemas import BaseSchema


class CreateAccountRequest(BaseSchema):
    login: str
    password: str


class UpdateAccountRequest(BaseSchema):
    login: str
    password: str
