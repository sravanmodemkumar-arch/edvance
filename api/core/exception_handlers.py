"""Global FastAPI exception handlers — consistent JSON error responses."""
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from shared.exceptions.auth_exceptions import (
    InsufficientPermissionsError,
    InvalidTokenError,
    NotFoundError,
    RateLimitError,
)


def _resp(code: int, message: str, request_id: str = "") -> JSONResponse:
    return JSONResponse(
        status_code=code,
        content={"success": False, "message": message, "request_id": request_id},
    )


def _rid(request: Request) -> str:
    return getattr(request.state, "request_id", "")


def register_handlers(app: FastAPI) -> None:
    @app.exception_handler(InvalidTokenError)
    async def _auth(req: Request, exc: InvalidTokenError):
        return _resp(status.HTTP_401_UNAUTHORIZED, str(exc), _rid(req))

    @app.exception_handler(InsufficientPermissionsError)
    async def _perm(req: Request, exc: InsufficientPermissionsError):
        return _resp(status.HTTP_403_FORBIDDEN, str(exc), _rid(req))

    @app.exception_handler(NotFoundError)
    async def _notfound(req: Request, exc: NotFoundError):
        return _resp(status.HTTP_404_NOT_FOUND, str(exc), _rid(req))

    @app.exception_handler(RateLimitError)
    async def _rate(req: Request, exc: RateLimitError):
        return _resp(status.HTTP_429_TOO_MANY_REQUESTS, str(exc), _rid(req))

    @app.exception_handler(RequestValidationError)
    async def _validation(req: Request, exc: RequestValidationError):
        return _resp(status.HTTP_422_UNPROCESSABLE_ENTITY, "Validation failed.", _rid(req))

    @app.exception_handler(Exception)
    async def _server(req: Request, exc: Exception):
        return _resp(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error.", _rid(req))
