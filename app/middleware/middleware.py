import time
from typing import Coroutine, Any, Callable

from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.openapi.models import Response
from starlette.requests import Request

from starlette.middleware.base import BaseHTTPMiddleware

from app.core.settings import settings


async def add_process_time_header(
        request: Request,
        call_next: Callable[[Request],
        Coroutine[Any, Any, Response]]
) -> Response:
    start_time = time.monotonic()
    response = await call_next(request)
    process_time = time.monotonic() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


middleware = [
    Middleware(BaseHTTPMiddleware, dispatch=add_process_time_header),
    Middleware(SessionMiddleware,
               max_age=60*60*24*3,
               secret_key=settings.SECRET_MIDDLEWARY),
]