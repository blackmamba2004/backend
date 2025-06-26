from app.schemas.requests.mixin import EmailMixin


class RegisterUserRequest(EmailMixin):
    password: str
    first_name: str
    last_name: str
    tel: str
    invite_token: str


class LoginRequest(EmailMixin):
    password: str
    public_key: str | None = None
