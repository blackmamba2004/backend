from app.schemas import BaseSchema


class RegisterUserDTO(BaseSchema):
    email: str
    password: str
    first_name: str
    last_name: str
    tel: str
    invite_token: str


class LoginDTO(BaseSchema):
    email: str
    password: str
    public_key: str | None
