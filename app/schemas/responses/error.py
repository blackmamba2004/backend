from app.schemas import BaseSchema


class ErrorResponse(BaseSchema):
    name: str
    message: str
