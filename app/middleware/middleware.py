from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

from app.core.settings import settings

middleware = [
    Middleware(SessionMiddleware,
               session_cookie='session',
               max_age=60*60*24*3,
               secret_key=settings.SECRET_MIDDLEWARY)
]