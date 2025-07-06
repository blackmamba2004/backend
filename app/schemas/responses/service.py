from app.schemas import BaseSchema
from uuid import UUID


class GetServiceResponse(BaseSchema):
    id: UUID
    name: str
