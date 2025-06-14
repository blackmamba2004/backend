from app.components.exceptions import ApplicationException


class BadRequestException(ApplicationException):
    """
    Bad Request
    """
    code = 400
    name = "Bad Request"


class IncorrectAuthHeaderException(BadRequestException):
    pass


class NotAuthHeaderException(BadRequestException):
    pass