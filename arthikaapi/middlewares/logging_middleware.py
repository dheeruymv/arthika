from urllib import response
from loguru import logger
import time

from starlette.middleware.base import BaseHTTPMiddleware



class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        time_start = time.time()
        logger.info("*****Inside Logger Middleware*****")
        logger.info(f"Request started at: {time_start} Request URL is: {request.url} \
                    Request coming from: {request.headers.get('host')}")
        response = await call_next(request)
        logger.info("*****End of Logger Middleware ******")
        time_end = time.time()
        logger.info(f"Request completed at : {time_end}, Total time taken: {(time_end-time_start)}")
        return response
