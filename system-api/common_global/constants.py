"""
constants.py

Responsibility:
- Hold application-wide constants
- Avoid magic strings and numbers
- Centralize values shared across layers
"""

# ===============================
# Application Metadata
# ===============================

APP_NAME = "aqi-system-api"
APP_VERSION = "1.0.0"

# ===============================
# HTTP / API Constants
# ===============================

DEFAULT_TIMEOUT_SECONDS = 5

# Standard headers
HEADER_AUTHORIZATION = "Authorization"
HEADER_CONTENT_TYPE = "Content-Type"

CONTENT_TYPE_JSON = "application/json"

# ===============================
# Authentication Constants
# ===============================

BEARER_PREFIX = "Bearer "

CLIENT_ID_HEADER = "my-client-id"
CLIENT_SECRET_HEADER = "my-secret"

# ===============================
# Downstream API Identifiers
# ===============================

SERVICE_WAQI = "WAQI"
SERVICE_OPENWEATHER = "OPENWEATHER"

# ===============================
# AQI Domain Constants
# ===============================

AQI_STATUS_GOOD = "GOOD"
AQI_STATUS_MODERATE = "MODERATE"
AQI_STATUS_POOR = "POOR"
AQI_STATUS_SEVERE = "SEVERE"
AQI_STATUS_HAZARDOUS = "HAZARDOUS"

# ===============================
# Error Codes (System API)
# ===============================

ERROR_INTERNAL = "INTERNAL_ERROR"
ERROR_VALIDATION = "VALIDATION_ERROR"

ERROR_WAQI_DOWN = "WAQI_SERVICE_UNAVAILABLE"
ERROR_OPENWEATHER_DOWN = "OPENWEATHER_SERVICE_UNAVAILABLE"
ERROR_CITY_NOT_FOUND = "CITY_NOT_FOUND"

INVALID_AUTHENTICATION_TOKEN = "INVALID_AUTHENTICATION_TOKEN"
RESOURCE_EXHAUSTED = "RESOURCE_EXHAUSTED"

# ===============================
# Logging Constants
# ===============================

LOG_CORRELATION_ID = "correlation_id"
LOG_SERVICE = "service"
LOG_PATH = "path"
LOG_METHOD = "method"

# ---- Service Names (for logging & tracing) ----
SERVICE_AQI = "AQI_SERVICE"
SERVICE_GEO = "GEO_SERVICE"