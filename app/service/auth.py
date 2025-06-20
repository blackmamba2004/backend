import logging

from fastapi import Request

from jwt import InvalidTokenError

from app.components import JWT
from app.components.exceptions import (
    EmailException, 
    TelException, 
    UnautorizedException,
    NotAuthHeaderException, 
    IncorrectAuthHeaderException,
    IncorrectTokenTypeException,
    InvalidTokenException, 
    TokenRevokedException,
    ForbiddenException,
    TokenOwnerNotFoundException
)
from app.components import RedisCache
from app.components.exceptions import UnautorizedException
from app.components.types import UserType, TokenType
from app.components.utils import verify_password, get_password_hash, from_unix_timestamp, now
from app.schemas.dto import (
    RegisterBrokerDTO,
    ResetPasswordDTO, 
    RegisterUserDTO,
    LoginDTO
)
from app.schemas.responses import TokenPairResponse, Response
from app.service.email import EmailService
from app.service.linker import LinkerService
from app.unit_of_work import AuthUnitOfWork


logger = logging.getLogger(__name__)


class AuthService:
    def __init__(
        self,
        unit_of_work: AuthUnitOfWork,
        email_service: EmailService,
        linker_service: LinkerService,
        redis_cache: RedisCache,
        jwt: JWT
    ):
        self._uow = unit_of_work
        self._email_service = email_service
        self._linker_service = linker_service
        self._redis_cache = redis_cache
        self._jwt = jwt
        
    async def register_broker(self, body: RegisterBrokerDTO):
        async with self._uow as uow:
            broker = await uow.broker_repository.find_one(
                email=body.email
            )

            if not broker:
                broker = await uow.broker_repository.create(
                    body, error=UnautorizedException
                )

            elif broker and broker.is_active:
                raise EmailException(message="This email is taken")

            await uow.commit()

        await self._send_email_with_token(
            broker.id, 
            UserType.BROKER.value, 
            body.email,
            "Регистрация",
            "Перейдите по ссылке для подтверждения аккаунта"
        )

        return Response(message="Confirm your email")

    async def register_user(self, body: RegisterUserDTO):
        payload = await self._verify_token_with_exceptions(
            body.invite_token, TokenType.INVITE.value
        )

        async with self._uow as uow:
            user = await uow.user_repository.find_one(
                email=body.email
            )

            if not user:
                user = await uow.broker_repository.create(
                    body, broker_id=payload["sub"], error=UnautorizedException
                )

            elif user and user.is_active:
                raise EmailException(message="This email is taken")

            await uow.commit()

        await self._send_email_with_token(
            user.id, 
            UserType.USER.value, 
            body.email, 
            "Регистрация", 
            "Перейдите по ссылке для подтверждения аккаунта"
        )
        return Response(message="Confirm your email")
    
    async def verify_email(self, token: str):
        payload = await self._verify_token_with_exceptions(
            token, TokenType.EMAIL.value
        )

        async with self._uow as uow:
            if payload["user_type"] == UserType.BROKER.value:
                broker = await uow.broker_repository.find_by_id(payload["sub"])
                if broker:
                    await uow.broker_repository.update(db_obj=broker, obj_in={"is_active": True})
            
            elif payload["user_type"] == UserType.USER.value:
                user = await uow.user_repository.find_by_id(payload["sub"])
                if user:
                    await uow.user_repository.update(db_obj=user, obj_in={"is_active": True})
        
            else:
                raise UnautorizedException("Incorrect user type")

            await uow.commit()

        expired = from_unix_timestamp(payload["exp"]) - now()

        await self._redis_cache.set(
            key_tuple=(payload["jti"]), 
            body={"revoked": True},
            ttl=int(expired.total_seconds())
        )
        return Response(message="Account is activated")
    
    async def login_broker(self, body: LoginDTO):
        async with self._uow as uow:
            broker = await uow.broker_repository.find_one(email=body.email)
            if not broker:
                raise UnautorizedException("Email is incorrect")
            
            if not verify_password(body.password, broker.hashed_password):
                raise UnautorizedException("Password is incorrect")
            
            if not broker.is_active:
                raise UnautorizedException("Account is not activated")
            
            access_token, refresh_token = self._jwt.issue_tokens_for_user(
                str(broker.id), user_type=UserType.BROKER.value
            )

            return TokenPairResponse(
                access_token=access_token,
                refresh_token=refresh_token
            )
    
    async def login_user(self, body: LoginDTO):
        async with self._uow as uow:
            logger.info(body.email)
            user = await uow.user_repository.find_one(email=body.email)
            if not user:
                raise UnautorizedException("Email is incorrect")
            
            if not verify_password(body.password, user.hashed_password):
                raise UnautorizedException("Password is incorrect")
            
            if not user.is_active:
                raise UnautorizedException("Account is not activated")
            
            access_token, refresh_token = self._jwt.issue_tokens_for_user(
                str(user.id), user_type=UserType.USER.value
            )

            await self._redis_cache.set(
                key_tuple=(user.id,),
                body={"public_key": body.public_key},
                ttl=int(self._jwt._config.refresh_token_ttl)
            )
            
            return TokenPairResponse(
                access_token=access_token,
                refresh_token=refresh_token
            )
    
    async def login(self, body: LoginDTO):
        if body.public_key is None:
            return await self.login_broker(body)
        
        return await self.login_user(body)

    async def check_access_token(
        self, request: Request, authorization_header: str, user_type: str
    ) -> None:
        """
        :param user_type: передаем UserType.BROKER.value | UserType.USER.value
        """
        clear_token = self.__try_to_get_clear_token(authorization_header)

        payload = await self._verify_token_with_exceptions(
            clear_token, TokenType.ACCESS.value
        )

        if payload["user_type"] != user_type:
            raise ForbiddenException("You have not enough permissions")
        
        async with self._uow as uow:
            if user_type == UserType.BROKER.value:
                broker = await uow.broker_repository.find_by_id(payload["sub"])
                if not broker:
                    raise TokenOwnerNotFoundException("Token owner is not found")
                request.state.broker = broker
                
            elif user_type == UserType.USER.value:
                user = await uow.user_repository.find_by_id(payload["sub"])
                if not user:
                    raise TokenOwnerNotFoundException("Token owner is not found")
                request.state.user = user

    async def refresh_tokens(self, refresh_token: str):
        payload = await self._verify_token_with_exceptions(
            refresh_token, TokenType.REFRESH.value
        )
        
        async with self._uow as uow:
            if payload["user_type"] == UserType.BROKER.value:
                user = await uow.broker_repository.find_by_id(payload["sub"])
                
            elif payload["user_type"] == UserType.USER.value:
                user = await uow.user_repository.find_by_id(payload["sub"])
            
            else:
                raise ForbiddenException("Incorrect user type")

        if not user:
            raise TokenOwnerNotFoundException("Token owner is not found")
        
        access_token, new_refresh_token = self._jwt.issue_tokens_for_user(
            str(user.id), user_type=payload["user_type"]
        )

        expired = from_unix_timestamp(payload["exp"]) - now()

        await self._redis_cache.set(
            key_tuple=(payload["jti"]), 
            body={"revoked": True},
            ttl=int(expired.total_seconds())
        )

        return TokenPairResponse(
            access_token=access_token, 
            refresh_token=new_refresh_token
        )
    
    async def logout(self, refresh_token: str):
        payload = await self._verify_token_with_exceptions(
            refresh_token, TokenType.REFRESH.value
        )
        
        async with self._uow as uow:
            if payload["user_type"] == UserType.BROKER.value:
                user = await uow.broker_repository.find_by_id(payload["sub"])
                
            elif payload["user_type"] == UserType.USER.value:
                user = await uow.user_repository.find_by_id(payload["sub"])

            else:
                raise ForbiddenException("Incorrect user type")

        if not user:
            raise TokenOwnerNotFoundException("Token owner is not found")

        expired = from_unix_timestamp(payload["exp"]) - now()
        
        await self._redis_cache.set(
            key_tuple=(payload["jti"]), 
            body={"revoked": True}, 
            ttl=int(expired.total_seconds())
        )

        return Response(message="Logged out")

    async def reset_password(self, email: str):
        """
        :param user_type: передаем UserType.BROKER.value | UserType.USER.value
        """
        async with self._uow as uow:
            user = await uow.broker_repository.find_one(email=email)
            user_type = UserType.BROKER
            if not user:
                user = await uow.user_repository.find_one(email=email)
                user_type = UserType.USER

        if not user:
            raise EmailException("Account with this email is not found")
        
        if not user.is_active:
            raise UnautorizedException("Account is not activated")
        
        await self._send_email_with_token(
            user.id, user_type, email, "Сброс пароля","Перейдите по ссылке для сброса пароля"
        )
        return Response(message="If an account with this email exists, we sent a password reset link.")
    
    async def reset_password_confirm(self, body: ResetPasswordDTO):
        payload = await self._verify_token_with_exceptions(
            body.email_token, TokenType.EMAIL.value
        )
        
        async with self._uow as uow:
            if payload["user_type"] == UserType.BROKER.value:
                user = await uow.broker_repository.find_by_id(payload["sub"])
                
            elif payload["user_type"] == UserType.USER.value:
                user = await uow.user_repository.find_by_id(payload["sub"])
                
            if not user:
                raise TokenOwnerNotFoundException("Token owner is not found")
        
            user.hashed_password = get_password_hash(body.password)

            await uow.commit()
        
        expired = from_unix_timestamp(payload["exp"]) - now()

        await self._redis_cache.set(
            key_tuple=(payload["jti"]), 
            body={"revoked": True},
            ttl=int(expired.total_seconds())
        )
        return Response(message="Password updated")
    
    async def invite_user(self, broker):
        invite_token = self._jwt.generate_invite_token(
            str(broker.id)
        )

        link = self._linker_service.create_user_invite_link(invite_token)

        return Response(message=link)

    async def _verify_token_with_exceptions(
        self,
        token: str,
        token_type: str,
    ) -> dict:
        try:
            payload = self._jwt.verify_token(token)
            if payload.get("token_type") != token_type:
                raise IncorrectTokenTypeException("Incorrect token type")
        except InvalidTokenError:
            raise InvalidTokenException("Token is invalid")

        jti = payload.get("jti")
        if jti:
            data = await self._redis_cache.get(key_tuple=(jti))
            if data is not None and data.get("revoked"):
                raise TokenRevokedException("Token revoked")
        
        return payload
    
    async def _send_email_with_token(
        self, user_id, user_type: str, email: str, subject: str, body: str
    ):
        """
        :param user_type: передаем UserType.BROKER.value | UserType.USER.value
        """
        email_token = self._jwt.generate_email_token(
            str(user_id), user_type=user_type
        )

        logger.info(f"Email token: {email_token}")

        link = self._linker_service.create_verify_link(email_token)

        await self._email_service.send_email(
            email, subject, f"<p>{body} {link}.</p>"
        )
    
    def __try_to_get_clear_token(self, authorization_header: str) -> str:
        if authorization_header is None:
            raise NotAuthHeaderException("AuthHeader must contain 'Bearer <token>'")

        if 'Bearer ' not in authorization_header:
            raise IncorrectAuthHeaderException("Bearer must contain in AuthHeader")

        return authorization_header.replace('Bearer ', '')
