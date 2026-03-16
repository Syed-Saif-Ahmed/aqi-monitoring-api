"""
global_error_handler.py 

responsiblility:
- catch and handle all unhandled exception 
- convert exceptions into standard api response
- prevent internal errors from leaking to customers 
"""
from typing import Optional
from fastapi import FastAPI


from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_503_SERVICE_UNAVAILABLE,
)

from common_global.logger import get_logger

logger = get_logger(__name__)

#------------------------------
# Custom Based Exception
#------------------------------

class BaseAPIException(Exception):
    def __init__(
            self,
            message: str,
            status_code: int = HTTP_500_INTERNAL_SERVER_ERROR,
            error_code: str = "INTERNAL_SERVER_ERROR",
            details: Optional[dict] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}

#------------------------------------------
# Exception handler
#------------------------------------------

async def base_api_exception_handler(
        request: Request,
        exc: BaseAPIException,
):
    logger.error(
        "handled API Exception",
        extra={
            "path": request.url.path,
            "method": request.method,
            "error_code": exc.error_code,
            "details": exc.details,
        },
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success":False,
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "details": exc.details,
            },
        },
    )

async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
):
    logger.warning(
        "Validation error",
        extra={
            "path": request.url.path,
            "error": exc.errors(),
        },
    )

    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={
            "success": False,
            "error":{
                "code": "VALIDATION_ERROR",
                "message": "Invalid request parameters",
                "details": exc.errors(),
            },
        },
    )

async def generic_exception_handler(
        request: Request,
        exc: Exception,

):
    logger.exception(
        "Unhandled exception occurred",
        extra={
            "path": request.url.path,
            "method": request.method,
        },
    )

    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "Something went wrong. Please try again later.",
            },
        },
    )

def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(BaseAPIException, base_api_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)