from pydantic import BaseModel


class SuccessResponse(BaseModel):
    data: object
    status: int


class ErrorResponse(BaseModel):
    error: str
    status: int
    details: dict | None = None
