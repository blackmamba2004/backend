from app.components.exceptions import ApplicationException


class NotFoundException(ApplicationException):
    """
    NotFound Error
    """
    code = 404
    name = "NotFound Error"
