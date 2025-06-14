from datetime import timedelta
from typing import Any
import uuid

import jwt

from app.config import JWTConfig
from app.components.types.jwt import TokenType
from app.components.utils import utcnow, to_unix_timestamp


class JWT:
    def __init__(self, config: JWTConfig):
        self._config = config

    def generate_unlimited_access_token(self, subject: str, **payload) -> str:
        return self.__sign_token(
            token_type=TokenType.ACCESS.value,
            subject=subject
            **payload
        )

    def generate_access_token(self, subject: str, **payload) -> str:
        return self.__sign_token(
            token_type=TokenType.ACCESS.value,
            subject=subject,
            ttl=self._config.access_token_ttl,
            **payload
        )

    def generate_refresh_token(self, subject: str, **payload) -> str:
        return self.__sign_token(
            token_type=TokenType.REFRESH.value,
            subject=subject,
            ttl=self._config.refresh_token_ttl,
            **payload
        )
    
    def generate_email_token(self, subject: str, **payload) -> str:
        return self.__sign_token(
            token_type=TokenType.EMAIL.value,
            subject=subject,
            ttl=self._config.email_token_ttl,
            **payload
        )
    
    def generate_invite_token(self, subject: str, **payload) -> str:
        return self.__sign_token(
            token_type=TokenType.INVITE.value,
            subject=subject,
            ttl=self._config.invite_token_ttl,
            **payload
        )

    def issue_tokens_for_user(self, subject: str, **payload) -> tuple[str, str]:
        return (self.generate_access_token(subject, **payload),
                self.generate_refresh_token(subject, **payload))
        
    def __sign_token(self, token_type: str, subject: str, ttl: int, **payload) -> str:
        current_timestamp = to_unix_timestamp(utcnow())
        data = dict(
            sub=subject,
            token_type=token_type,
            exp=current_timestamp + ttl,
            jti=self.__generate_jti(),
        )
        payload.update(data)
        return jwt.encode(payload, self._config.secret_key, algorithm=self._config.algorithm)

    @staticmethod
    def __generate_jti() -> str:
        return str(uuid.uuid4())

    def verify_token(self, token: str) -> dict[str, Any]:
        return jwt.decode(token, self._config.secret_key, algorithms=[self._config.algorithm])

    def get_jti(self, token) -> str:
        return self.verify_token(token)['jti']

    def get_sub(self, token) -> str:
        return self.verify_token(token)['sub']

    def get_exp(self, token) -> int:
        return self.verify_token(token)['exp']

    @staticmethod
    def get_raw_jwt(token) -> dict[str, Any]:
        """
        Возвращает полезную нагрузку токена, не проверяя, истек ли токен
        """
        return jwt.decode(token, options={'verify_signature': False})
