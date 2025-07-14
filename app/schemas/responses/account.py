from app.schemas import BaseSchema
from uuid import UUID


class GetAccountResponse(BaseSchema):
    id: UUID
    service_id: UUID


class GetEncryptedAccountData(BaseSchema):
    data: str
