from app.components.exceptions import ApplicationException


class ForbiddenException(ApplicationException):
    """
    Forbidden Error
    """
    code = 403
    name = "Forbidden Error"


class IncorrectTokenTypeException(ForbiddenException):
    pass


class InvalidTokenException(ForbiddenException):
    pass


class TokenRevokedException(ForbiddenException):
    pass


class TokenOwnerNotFoundException(ForbiddenException):
    pass
