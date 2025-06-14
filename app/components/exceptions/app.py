class ApplicationException(Exception):
    """
    Базовый класс исключения приложения
    """

    code: int = 500
    name: str = "Internal Server Error"

    def __init__(self, message: str = None):
        self.message = message
        super().__init__(self.message)
