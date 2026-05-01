from starlette.middleware import Middleware
from .logging_middleware import LoggingMiddleware

middlewares = [Middleware(LoggingMiddleware)]