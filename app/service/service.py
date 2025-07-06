import logging

from uuid import UUID

from jwt import InvalidTokenError

from app.components.exceptions import (
    EmailException,
    UnautorizedException,
    NotAuthHeaderException, 
    IncorrectAuthHeaderException,
    IncorrectTokenTypeException,
    InvalidTokenException, 
    TokenRevokedException,
    ForbiddenException,
    TokenOwnerNotFoundException
)
from app.schemas.dto import (
    CreateServiceDTO, 
    UpdateServiceDTO
)
from app.schemas.responses import TokenPairResponse, Response
from app.unit_of_work import ServiceUnitOfWork


logger = logging.getLogger(__name__)


class Service:
    def __init__(
        self,
        unit_of_work: ServiceUnitOfWork,
    ):
        self._uow = unit_of_work

    async def create_service(self, body: CreateServiceDTO):
        async with self._uow as uow:
            service = await uow.service_repository.create(body)
            await uow.commit()
        return service
    
    async def get_service(self, service_id: UUID):
        async with self._uow as uow:
            return await uow.service_repository.find_by_id(
                service_id, exception_on_none=True
            )
        
    async def get_all_services(self):
        async with self._uow as uow:
            return await uow.service_repository.find_all()
        
    async def update_service(self, service_id: UUID, body: UpdateServiceDTO):
        async with self._uow as uow:
            service = await uow.service_repository.find_by_id(
                service_id, exception_on_none=True
            )
            updated_service = await uow.service_repository.update(
                db_obj=service, obj_in=body
            )
            await uow.commit()

        return updated_service
    
    async def delete_service(self, service_id: UUID):
        async with self._uow as uow:
            await uow.service_repository.delete_by_id(service_id)
            await uow.commit()

        return Response(message="Service was succesfully deleted")
        
    # async def register(self, body, **extra_model_fields):
    #     """
    #     :param user_role: передаем UserRole.BROKER | UserRole.USER
    #     """
    #     async with self._uow as uow:
    #         user = await uow.user_repository.find_one(
    #             email=body.email
    #         )

    #         if user and user.is_active:
    #             raise EmailException(message="This email is taken")

    #         elif not user:
    #             user = await uow.user_repository.create(
    #                 body, **extra_model_fields
    #             )

    #         await uow.commit()

    #     await self._send_email_with_token(
    #         user.id,
    #         body.email,
    #         "Регистрация",
    #         "Перейдите по ссылке для подтверждения аккаунта"
    #     )

    #     return Response(message="Confirm your email")

    # async def verify_email(self, token: str):
    #     payload = await self._verify_token_with_exceptions(
    #         token, TokenType.EMAIL.value
    #     )

    #     async with self._uow as uow:
    #         user = await uow.user_repository.find_by_id(payload["sub"])
    #         if user:
    #             await uow.user_repository.update(db_obj=user, obj_in={"is_active": True})

    #         await uow.commit()

    #     expired = from_unix_timestamp(payload["exp"]) - now()

    #     await self._redis_cache.set(
    #         key_tuple=(payload["jti"]), 
    #         body={"revoked": True},
    #         ttl=int(expired.total_seconds())
    #     )
    #     return Response(message="Account is activated")
    
    # async def login(self, body: LoginDTO):
    #     async with self._uow as uow:
    #         user = await uow.user_repository.find_one(email=body.email)

    #         if not user:
    #             raise UnautorizedException("Email is incorrect")
            
    #         if not verify_password(body.password, user.hashed_password):
    #             raise UnautorizedException("Password is incorrect")
            
    #         if not user.is_active:
    #             raise UnautorizedException("Account is not activated")
            
    #         access_token, refresh_token = self._jwt.issue_tokens_for_user(str(user.id))

    #         await self._redis_cache.set(
    #             key_tuple=(user.id,),
    #             body={"public_key": body.public_key},
    #             ttl=int(self._jwt._config.refresh_token_ttl)
    #         )
            
    #         return TokenPairResponse(
    #             access_token=access_token,
    #             refresh_token=refresh_token
    #         )

    # async def check_access_token(
    #     self, user_role: UserRole
    # ) -> User:
    #     """
    #     :param user_role: передаем UserRole.BROKER | UserRole.USER
    #     """

    #     auth_header = self._request.headers.get("Authorization")

    #     clear_token = self.__try_to_get_clear_token(auth_header)

    #     payload = await self._verify_token_with_exceptions(
    #         clear_token, TokenType.ACCESS.value
    #     )

    #     async with self._uow as uow:
    #         user = await uow.user_repository.find_by_id(payload["sub"])

    #         if not user:
    #             raise TokenOwnerNotFoundException("Token owner is not found")
            
    #         if user.role != user_role:
    #             raise ForbiddenException("You have not enough permissions")
            
    #     return user

    # async def check_admin_access_token(self) -> User:
    #     return await self.check_access_token(UserRole.ADMIN)

    # async def check_broker_access_token(self) -> User:
    #     return await self.check_access_token(UserRole.BROKER)

    # async def check_client_access_token(self) -> User:
    #     return await self.check_access_token(UserRole.USER)
    
    # async def refresh_tokens(self, refresh_token: str):
    #     payload = await self._verify_token_with_exceptions(
    #         refresh_token, TokenType.REFRESH.value
    #     )
        
    #     async with self._uow as uow:
    #         user = await uow.user_repository.find_by_id(payload["sub"])

    #     if not user:
    #         raise TokenOwnerNotFoundException("Token owner is not found")
        
    #     access_token, new_refresh_token = self._jwt.issue_tokens_for_user(str(user.id))

    #     expired = from_unix_timestamp(payload["exp"]) - now()

    #     await self._redis_cache.set(
    #         key_tuple=(payload["jti"]), 
    #         body={"revoked": True},
    #         ttl=int(expired.total_seconds())
    #     )

    #     return TokenPairResponse(
    #         access_token=access_token, 
    #         refresh_token=new_refresh_token
    #     )
    
    # async def logout(self, refresh_token: str):
    #     payload = await self._verify_token_with_exceptions(
    #         refresh_token, TokenType.REFRESH.value
    #     )
        
    #     async with self._uow as uow:
    #         user = await uow.user_repository.find_by_id(payload["sub"])
        
    #     if not user:
    #         raise TokenOwnerNotFoundException("Token owner is not found")

    #     expired = from_unix_timestamp(payload["exp"]) - now()
        
    #     await self._redis_cache.set(
    #         key_tuple=(payload["jti"]), 
    #         body={"revoked": True}, 
    #         ttl=int(expired.total_seconds())
    #     )

    #     return Response(message="Logged out")

    # async def reset_password(self, email: str):
    #     async with self._uow as uow:
    #         user = await uow.user_repository.find_one(email=email)

    #     if not user:
    #         raise EmailException("Account with this email is not found")
        
    #     if not user.is_active:
    #         raise UnautorizedException("Account is not activated")
        
    #     await self._send_email_with_token(
    #         user.id, email, "Сброс пароля","Перейдите по ссылке для сброса пароля"
    #     )
    #     return Response(message="If an account with this email exists, we sent a password reset link.")
    
    # async def reset_password_confirm(self, body: ResetPasswordDTO):
    #     payload = await self._verify_token_with_exceptions(
    #         body.email_token, TokenType.EMAIL.value
    #     )
        
    #     async with self._uow as uow:
    #         user = await uow.user_repository.find_by_id(payload["sub"])
                
    #         if not user:
    #             raise TokenOwnerNotFoundException("Token owner is not found")
        
    #         user.hashed_password = get_password_hash(body.password)

    #         await uow.commit()
        
    #     expired = from_unix_timestamp(payload["exp"]) - now()

    #     await self._redis_cache.set(
    #         key_tuple=(payload["jti"]), 
    #         body={"revoked": True},
    #         ttl=int(expired.total_seconds())
    #     )
    #     return Response(message="Password updated")
    
    # async def invite_user(self, broker):
    #     invite_token = self._jwt.generate_invite_token(
    #         str(broker.id)
    #     )

    #     link = self._linker_service.create_user_invite_link(invite_token)

    #     return Response(message=link)

    # async def _verify_token_with_exceptions(
    #     self,
    #     token: str,
    #     token_type: str,
    # ) -> dict:
    #     try:
    #         payload = self._jwt.verify_token(token)
    #         if payload.get("token_type") != token_type:
    #             raise IncorrectTokenTypeException("Incorrect token type")
    #     except InvalidTokenError:
    #         raise InvalidTokenException("Token is invalid")

    #     jti = payload.get("jti")
    #     if jti:
    #         data = await self._redis_cache.get(key_tuple=(jti))
    #         if data is not None and data.get("revoked"):
    #             raise TokenRevokedException("Token revoked")
        
    #     return payload
    
    # async def _send_email_with_token(
    #     self, user_id, email: str, subject: str, body: str
    # ):
    #     """
    #     :param user_type: передаем UserType.BROKER.value | UserType.USER.value
    #     """
    #     email_token = self._jwt.generate_email_token(str(user_id))

    #     logger.info(f"Email token: {email_token}")

    #     link = self._linker_service.create_verify_link(email_token)

    #     await self._email_service.send_email(
    #         email, subject, f"<p>{body} {link}.</p>"
    #     )
    
    # def __try_to_get_clear_token(self, authorization_header: str) -> str:
    #     if authorization_header is None:
    #         raise NotAuthHeaderException("AuthHeader must contain 'Bearer <token>'")

    #     if 'Bearer ' not in authorization_header:
    #         raise IncorrectAuthHeaderException("Bearer must contain in AuthHeader")

    #     return authorization_header.replace('Bearer ', '')
