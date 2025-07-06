from app.schemas import BaseSchema


class CreateServiceDTO(BaseSchema):
    name: str


class UpdateServiceDTO(BaseSchema):
    name: str
