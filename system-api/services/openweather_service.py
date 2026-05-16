"""
Docstring for system-api.services.openweather_service

Responsibility:
- Interact with OpenWeather Geocoding API
- resolve city name to latitude and longitude 
- provide clean geo data to other service 
"""

from typing import Dict, Any

from config_loader import load_config
from common_global.http_client import get as http_get
from common_global.logger import get_logger
from common_global.constants import (
    SERVICE_OPENWEATHER,
    ERROR_OPENWEATHER_DOWN,
    ERROR_CITY_NOT_FOUND,
    INVALID_AUTHENTICATION_TOKEN,
)

from error.global_error_handler import BaseAPIException
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_503_SERVICE_UNAVAILABLE,
)

logger = get_logger(__name__)
_config = load_config()

def get_coordinates_by_city(city: str) -> Dict[str, float]:
    """
    Docstring for get_coordinates_by_city
    resolve latitude and longitude for a given  city.

    args:
        city name
    return
        dict {lat, lon}
    """

    url = (_config["openweather"]["base_url"] + _config["openweather"]["endpoints"]["geo"])
    api_key = _config["openweather"]["appid"]

    logger.info(
        f"calling openweather Geocoding API: City : {city}".format(city=city)
    )

    try: 
        response = http_get(
            url=url,
            params={
                "q":city,
                "limit": 1,
                "appid": api_key,
            },
        )
    except Exception as exc:
        logger.exception("Openweather API call failed")
        payload = response.json()
        raise _openweather_unavailable_error(exc) from exc
    

    return _handle_openweather_response(response)


# Internal Helpers

def _handle_openweather_response(response) -> Dict[str, Any]:
    """validate and extracts WAQi response"""
    
    if response.status_code == 200 and response.json() == []:
        logger.error(
            "Resource Not Found {status}".format(status=response.status_code)
        )
        raise _openweather_unavailable_error(response.json())


    payload = response.json()

    if response.status_code != 200:
        logger.error(
            "Openeather API returned non-200 response status code {status}".format(status=response.status_code)
        )
        raise _openweather_unavailable_error(payload)
    
    # This section might not be necessary
    if not isinstance(payload, list):
        logger.warning(
            "WAQI API returned error status",
            extra=payload,
        )
        raise _openweather_unavailable_error(payload)
    # this Section end
    
    return payload

def _openweather_unavailable_error(payload) -> BaseAPIException:

    if payload == []:
        raise BaseAPIException(
            message= "City Not found",
            status_code=HTTP_404_NOT_FOUND,
            error_code=ERROR_CITY_NOT_FOUND,
            details=payload,
        )
    
    elif payload.get("cod") == 401:
        raise BaseAPIException(
            message="Authentication failed: Invalid token",
            status_code=payload.get("cod"),
            error_code=INVALID_AUTHENTICATION_TOKEN,
            details=payload,
        )
    

    raise BaseAPIException(
        message="OpenWeather service is currently unavailable",
        status_code=HTTP_503_SERVICE_UNAVAILABLE,
        error_code=ERROR_OPENWEATHER_DOWN,
        details=payload,
    )