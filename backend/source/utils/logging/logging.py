import os
import logging
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

log_directory = os.path.join(os.path.dirname(__file__), '../../logs')
os.makedirs(log_directory, exist_ok=True)

log_path = os.path.join(log_directory, 'logs.log')

logging.basicConfig(
    filename=log_path,
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s:%(name)s:%(message)s"
)

logger = logging.getLogger("app_logger")

class AutoLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        method = request.method
        path = request.url.path
        client_ip = request.client.host

        logger.info(f"Request STARTED: {method} {path} from {client_ip}")
        start_time = time.time()

        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(f"ERROR on {method} {path}: {str(e)}")
            raise e

        process_time = round(time.time() - start_time, 3)
        status = response.status_code

        logger.info(f"Request ENDED: {method} {path} - Status {status} - {process_time}s")

        return response
