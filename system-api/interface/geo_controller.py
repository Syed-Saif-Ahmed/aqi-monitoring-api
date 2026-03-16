"""
geo_controller.py

Interface Layer (System API)

Responsibilities:
- Accept HTTP requests related to geo data
- Validate input parameters
- Delegate to OpenWeather service
- Return structured response

NO business logic.
NO external API calls.
"""

from fastapi import APIRouter, Path

from services.openweather_service import get_coordinates_by_city
from common_global.logger import get_logger
from common_global.constants import SERVICE_GEO

router = APIRouter(
    prefix="/api/v1/geo",
    tags=["GEO"],
)

logger = get_logger(__name__)


# ---------------------------------------------------------
# Fetch Latitude & Longitude using City Name
# Example: /api/v1/geo/Delhi
# ---------------------------------------------------------
@router.get("/{city}")
def fetch_coordinates_by_city(
    city: str = Path(
        ...,
        min_length=2,
        description="City name (e.g., Delhi, London)",
    )
):
    """
    Fetch geographic coordinates (latitude & longitude)
    using city name.

    Delegates directly to OpenWeather service.
    """

    logger.info(
        f"Geo request received City : {city}".format(city=city)
    )

    coordinates = get_coordinates_by_city(city)

    return {
        "request_type": "city",
        "city": city,
        "data": coordinates,
    }
