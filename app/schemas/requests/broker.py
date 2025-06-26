from app.schemas.requests.mixin import EmailMixin


class RegisterBrokerRequest(EmailMixin):
    password: str
    first_name: str
    last_name: str
    tel: str
