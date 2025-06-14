from app.components.exceptions import ApplicationException


class UnautorizedException(ApplicationException):
    """
    Unauthorized Error
    """
    code = 401
    name = "Unauthorized Error"


class EmailException(UnautorizedException):
    pass


class TelException(UnautorizedException):
    pass

