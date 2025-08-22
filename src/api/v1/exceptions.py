from fastapi import HTTPException


class BaseHTTPException(HTTPException):
    """
    Base HTTP exception class.
    """

    status_code = 500
    detail = "Internal Server Error"

    def __init__(self, detail: str = "Internal Server Error") -> None:
        super().__init__(status_code=self.status_code, detail=detail)


class BadRequestException(BaseHTTPException):
    """
    Bad request exception class.
    """

    status_code = 400
    detail = "Bad Request"


class NotFoundException(BaseHTTPException):
    """
    Not found exception class.
    """

    status_code = 404
    detail = "Not Found"
