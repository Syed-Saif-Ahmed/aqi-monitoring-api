"""
aqi_controller.py

Interface Layer (System API)

Responsibilities:
- Accept HTTP requests
- Validate input parameters
- Delegate to WAQI service
- Return structured responses

NO business logic.
NO external API calls.
"""

from fastapi import APIRouter, Query, Path

from services.waqi_service import get_aqi_by_city, get_aqi_by_geo
from common_global.logger import get_logger
from common_global.constants import SERVICE_AQI

router = APIRouter(
    prefix="/api/v1/aqi",
    tags=["AQI"],
)

logger = get_logger(__name__)


# ---------------------------------------------------------
# Fetch AQI using CITY (Path Parameter)
# Example: /api/v1/aqi/Delhi
# ---------------------------------------------------------
@router.get("/{city}")
def fetch_aqi_by_city(
    city: str = Path(
        ...,
        min_length=2,
        description="City name (e.g., Delhi, London)",
    )
):
    """
    Fetch AQI using city name.
    Delegates directly to WAQI service.
    """

    logger.info(
        f"AQI request received (city): {city}".format(city=city)
    )

    aqi_data = get_aqi_by_city(city)

    return {
        "request_type": "city",
        "city": city,
        "aqi": aqi_data,
    }


# ---------------------------------------------------------
# Fetch AQI using LAT & LON (Query Parameters)
# Example: /api/v1/aqi?lat=28.6&lon=77.2
# ---------------------------------------------------------
@router.get("")
def fetch_aqi_by_geo(
    lat: float = Query(
        ...,
        ge=-90,
        le=90,
        description="Latitude value",
    ),
    lon: float = Query(
        ...,
        ge=-180,
        le=180,
        description="Longitude value",
    ),
):
    """
    Fetch AQI using latitude and longitude.
    Delegates directly to WAQI service.
    """

    logger.info(
        f"AQI request received (geo) : latitude : {lat} | longitude : {lon}".format(lat=lat, lon=lon)
    )

    aqi_data = get_aqi_by_geo(lat=lat, lon=lon)

    return {
        "request_type": "geo",
        "coordinates": {
            "lat": lat,
            "lon": lon,
        },
        "aqi": aqi_data,
    }
