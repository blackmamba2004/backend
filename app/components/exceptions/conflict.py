from app.components.exceptions import ApplicationException


class ConflictException(ApplicationException):
    """
    Conflict Error
    """
    code = 409
    name = "Conflict Error"

