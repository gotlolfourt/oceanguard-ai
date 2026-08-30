from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


class AppError(HTTPException):
    def __init__(self, status_code: int, error: str, details: dict | None = None):
        super().__init__(status_code=status_code, detail={"error": error, "status": status_code, "details": details})


def success_response(data: object, status: int = 200) -> dict:
    return {"data": data, "status": status}


async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content=exc.detail)


async def generic_error_handler(_: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=500, content={"error": "Internal server error", "status": 500, "details": {"message": str(exc)}})
