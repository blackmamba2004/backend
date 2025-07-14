from app.schemas import BaseSchema


class ChangeUserPermissionsRequest(BaseSchema):
    can_trade: bool
