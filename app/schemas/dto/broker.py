from app.schemas import BaseSchema


class RegisterBrokerDTO(BaseSchema):
    email: str
    password: str
    first_name: str
    last_name: str
    tel: str


class LoginBrokerDTO(BaseSchema):
    email: str
    password: str
