from fastapi import HTTPException


class BaseHTTPException(HTTPException):
    status_code = 500
    detail = "Internal Server Error"

    def __init__(self, detail: str = "Internal Server Error") -> None:
        super().__init__(status_code=self.status_code, detail=detail)


class BadRequestException(BaseHTTPException):
    status_code = 400
    detail = "Bad Request"


class NotFoundException(BaseHTTPException):
    status_code = 404
    detail = "Not Found"
