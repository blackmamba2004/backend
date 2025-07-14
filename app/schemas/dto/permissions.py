from app.schemas import BaseSchema


class ChangeUserPermissionsDTO(BaseSchema):
    can_trade: bool
