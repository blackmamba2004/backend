from app.components.exceptions import ApplicationException

class UniqueConstraintViolationError(ApplicationException):
    code = 400
    name = "Unique error"
