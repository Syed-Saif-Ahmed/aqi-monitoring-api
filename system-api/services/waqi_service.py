"""
Docstring for system-api.services.waqi_service

Responsibilities:
- interact with WAQI external API 
- Fetch AQI data using city name OR geo coordinate
- handle downstream failures gracefully 
"""

from typing import Dict, Any

from config_loader import load_config
from common_global.http_client import get as http_get
from common_global.logger import get_logger
from common_global.constants import (
    SERVICE_WAQI,
    ERROR_WAQI_DOWN,
    INVALID_AUTHENTICATION_TOKEN,
    ERROR_CITY_NOT_FOUND,
    RESOURCE_EXHAUSTED,
)

from error.global_error_handler import BaseAPIException
from starlette.status import HTTP_503_SERVICE_UNAVAILABLE, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN

logger = get_logger(__name__)
_config = load_config()

def get_aqi_by_city(city: str) -> Dict[str,Any]:
    """
    Docstring for get_aqi_by_city

    Fetch AQI details using city name 
    
    :param city: City name
    :type city: str
    :return: AQI REsponse
    :rtype: Dict[str, Any]
    """

    url = (_config["external_services"]["waqi"]["base_url"] + _config["external_services"]["waqi"]["endpoints"]["city_feed"]).format(city=city)
    token = _config["external_services"]["waqi"]["token"]

    logger.info(
        f"Calling WAQI AQI by Cty: {city}".format(city=city),
    )

    try:
        response = http_get(
            url=url,
            params={"token": token},
        )
    except Exception as exc:
        logger.exception("WAQI city API call failed")
        payload = response.json()
        raise _waqi_unavailable_error(exc) from exc
    
    return _handle_waqi_response(response)

def get_aqi_by_geo(lat: float, lon: float) -> Dict[str, Any]:
    """ Fetch AQI details using latitude and longitude .
    ARgs:
        lat: Latitude
        lon: longitude
    return: 
        Dict[str, any]: AQI response
    """

    url = (_config["external_services"]["waqi"]["base_url"] + _config["external_services"]["waqi"]["endpoints"]["geo_feed"]).format(lat=lat, lon=lon)
    token = _config["external_services"]["waqi"]["token"]

    logger.info(
        "Calling WAQI API by geo :: latitude : {lat} | longitude : {lon}".format(lon=lon, lat=lat)
    )

    try:
        response = http_get(
            url=url,
            params={
                "token": token,
            },
        )
    except Exception as exc:
        logger.exception("WAQI geo API call failed")
        payload = response.json()
        raise _waqi_unavailable_error(payload) from exc
    
    return _handle_waqi_response(response)

# INTERNAL HELPERS 


def _handle_waqi_response(response) -> Dict[str, Any]:
    """validate and extracts WAQi response"""

    payload = response.json()

    if response.status_code != 200:
        logger.error(
            "WAQI API returned non-200 response",
            extra={
                "status": response.status_code,
                "message":payload,
            },
        )
        raise _waqi_unavailable_error(payload)


    elif payload.get("status") != "ok":
        logger.warning(
            "WAQI API returned error status",
            extra=payload,
        )
        raise _waqi_unavailable_error(payload)
    
    return payload.get("data", {})

def _waqi_unavailable_error(payload):
    """
    Docstring for _waqi_unavailable_error
    Standard WAQI unavailable error 
    """
    if payload.get("status") is not None and payload.get("status") == "error":
        if payload.get("data") == "Invalid key":
            return BaseAPIException(
                message="Authentication failed: Invalid token",
                status_code=HTTP_401_UNAUTHORIZED,
                error_code=INVALID_AUTHENTICATION_TOKEN,
                details=payload,
            )
        elif payload.get("data") == "Unknown city":
            return BaseAPIException(
                message="Resource Not Found",
                status_code=HTTP_404_NOT_FOUND,
                error_code=ERROR_CITY_NOT_FOUND,
                details=payload,
            )
        elif payload.get("data") == "Over quota":
            return BaseAPIException(
                message="You have exceeded your request quota",
                status_code=HTTP_403_FORBIDDEN,
                error_code=RESOURCE_EXHAUSTED,
                details=payload,
            )
        return BaseAPIException(
            message="WAQI service is currently unavaliable",
            status_code=HTTP_503_SERVICE_UNAVAILABLE,
            error_code=ERROR_WAQI_DOWN,
            details=payload,

        )
