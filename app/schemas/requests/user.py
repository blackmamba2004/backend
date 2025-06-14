from pydantic import EmailStr

from app.schemas import BaseSchema


class RegisterUserRequest(BaseSchema):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    tel: str
    invite_token: str


class LoginUserRequest(BaseSchema):
    email: str
    password: str
    public_key: str
