from pydantic import EmailStr

from app.schemas import BaseSchema


class RegisterBrokerRequest(BaseSchema):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    tel: str
