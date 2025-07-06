from app.schemas import BaseSchema


class CreateServiceRequest(BaseSchema):
    name: str


class UpdateServiceRequest(BaseSchema):
    name: str
