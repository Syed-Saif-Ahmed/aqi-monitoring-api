"""
main.py

Application entry point.

Responsibilities:
- Create FastAPI app
- Register routers
- Register global exception handlers
- Load environment configuration
"""

from fastapi import FastAPI


from interface.aqi_controller import router as aqi_router
from interface.geo_controller import router as geo_router
from error.global_error_handler import register_exception_handlers
from config_loader import load_config
from common_global.logger import get_logger
from common_global.constants import APP_NAME, APP_VERSION
from security.client_auth import security_middleware


# ---------------------------------------------------------
# Load Configuration
# ---------------------------------------------------------
config = load_config()

logger = get_logger(__name__)


# ---------------------------------------------------------
# Create FastAPI Application
# ---------------------------------------------------------
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="System API for AQI and Geo services",
)


app.middleware("http")(security_middleware)


# ---------------------------------------------------------
# Register Routers
# ---------------------------------------------------------
app.include_router(aqi_router)
app.include_router(geo_router)


# ---------------------------------------------------------
# Register Global Exception Handlers
# ---------------------------------------------------------
register_exception_handlers(app)


# ---------------------------------------------------------
# Startup Event
# ---------------------------------------------------------
@app.on_event("startup")
def startup_event():
    logger.info("Application started successfully")


# ---------------------------------------------------------
# Health Check (Recommended for production)
# ---------------------------------------------------------
@app.get("/health")
def health_check():
    return {"status": "UP"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)