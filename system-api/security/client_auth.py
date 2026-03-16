import uuid
from fastapi import Request, HTTPException
from starlette.responses import Response

from config_loader import load_config
from common_global.logger import get_logger

from fastapi.responses import JSONResponse


config = load_config()
logger = get_logger(__name__)


async def security_middleware(request: Request, call_next):
    """
    Middleware to:
    - Enforce client_id & client_secret
    - Generate or read correlation_id
    """

    # -----------------------------------------------------
    # Correlation ID Handling
    # -----------------------------------------------------
    correlation_id = request.headers.get(
        "X-Correlation-ID", str(uuid.uuid4())
    )

    request.state.correlation_id = correlation_id

    # -----------------------------------------------------
    # Client Credential Enforcement
    # -----------------------------------------------------
    client_id = request.headers.get("client-id")
    client_secret = request.headers.get("client-secret")

    if client_id != config["security"]["client_id"] or client_secret != config["security"]["client_secret"]:
        logger.warning(
            "Unauthorized access attempt",
            extra={"correlation_id": correlation_id}
        )

        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "error": {
                    "code": "UNAUTHORIZED",
                    "message": "Invalid client credentials"
                },
                "correlation_id": request.state.correlation_id
            }
        )
        raise HTTPException(status_code=401, detail="Invalid client credentials")

    # -----------------------------------------------------
    # Continue Request
    # -----------------------------------------------------
    response: Response = await call_next(request)

    # Attach Correlation ID to response header
    response.headers["X-Correlation-ID"] = correlation_id

    return response