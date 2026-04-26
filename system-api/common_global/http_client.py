"""
Docstring for system-api.global.http_client

http_client.py 

Responsibility: 
 - Handel outbound HTTP calls
 - Apply timeouts, retries, and header consistently
 - Abstract request library usage 
"""

import requests
from typing import Any, Dict, Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config_loader import load_config 

_config = load_config()

def _build_session() -> requests.Session:
    """
    Docstring for _build_session
    Build a request session with retry strategy.

    :return: requests.Session
    :rtype: object
    """

    retry_config = _config.get("http", {}).get("retry",{})

    retries = Retry(
        total = retry_config.get("total",3),
        backoff_factor=retry_config.get("backoff_factor", 0.3),
        status_forcelist=retry_config.get("status_forcelist",[500,502,503,504]),
        allowed_methods=["GET","POST","PUT","DELETE","PATCH"],
        raise_on_status=False
    )

    adapter = HTTPAdapter(max_retries=retries)

    session = requests.Session()
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session

_session = _build_session()

def get(
        url: str,
        headers: Optional[Dict[str,str]] = None,
        params: Optional[Dict[str,Any]] = None,
        timeout: Optional[float] = None,
 ) -> requests.Response:
    """
    HTTP GET Request
    """

    return _session.get(
        url=url,
        headers=headers,
        params=params,
        timeout=timeout or _default_timeout(),
    )

def post(
        url=str,
        headers: Optional[Dict[str,str]] = None,
        params: Optional[Dict[str,Any]] = None,
        timeout: Optional[float] = None,
        json: Optional[Dict[str,Any]] = None,
        data: Optional[Any] = None,
) -> requests.Response:
    """
    HTTP POST Request
    """

    return _session.post(
        url=url,
        headers=headers,
        params=params,
        timeout=timeout or _default_timeout(),
        data=data,
        json=json,
    )

def put(
        url: str,
        headers: Optional[Dict[str,str]] = None,
        params: Optional[Dict[str,Any]] = None,
        timeout: Optional[float] = None,
        json: Optional[Dict[str,Any]] = None,
) -> requests.Response:
    """ HTTP PUT Response """

    return _session.put(
        url=url,
        headers=headers,
        params=params,
        timeout=timeout or _default_timeout(),
        json=json,
    )

def delete(
        url: str,
        headers: Optional[Dict[str,str]] = None,
        params: Optional[Dict[str,Any]] = None,
        timeout: Optional[float] = None,
        json: Optional[Dict[str,Any]] = None,
) -> requests.Response:
    """HTTP DELETE Response"""

    return _session.delete(
        url=url,
        headers=headers,
        params=params,
        timeout=timeout or _default_timeout(),
        json=json,
    )

def _default_timeout() -> float:
    """
    fetch default timeout from config
    """

    return _config.get("http",{}).get("timeout_seconds",5)
