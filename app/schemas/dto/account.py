from app.schemas import BaseSchema


class CreateAccountDTO(BaseSchema):
    login: str
    password: str


class UpdateAccountDTO(BaseSchema):
    login: str
    password: str
