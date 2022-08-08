from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.responses import JSONResponse
from fastapi import Request


def authjwt_exception_handler(request: Request, e: AuthJWTException):
    return JSONResponse(
        status_code=e.status_code,
        content={"detail": e.message}
    )