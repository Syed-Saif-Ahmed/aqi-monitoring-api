"""
Config loader file:

Responsibility:
- load and merge configuration files
- resolve active environments
- returns single immutable config object 
"""

import os
import yaml
from typing import Any, Dict
from functools import lru_cache

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR,"config")
COMMON_CONFIG_DIR = os.path.join(CONFIG_DIR,"common.yaml")

def _read_yaml(file_path: str) -> Dict[str, Any]:
    """
    Read a YAML file and return the result

    Args:
        file_path(str): Absolute path to the YAML file.

    Return:
        dict: Parsed YAML content

    Raise:
        RuntimeError: if file is missing or invalid. 
    """

    try:
        with open(file_path,"r") as file:
            return yaml.safe_load(file) or {}
    except FileNotFoundError:
        raise RuntimeError(f"Configuration file not found: {file_path}")
    except yaml.YAMLError as e:
        raise RuntimeError(f"Invalid YAML in configuration file: {file_path} Error: {e}")
    
@lru_cache(maxsize=1)
def load_config() -> Dict[str, Any]:
    """
    Loads and merges common and environment-specific configuration.

    Orders of precedence:
    1. common.yaml
    2. <env>.yaml

    Environment is resolved using:
    - APP_ENV environment variable 
    - Default to 'dev'

    Return:
        dict: Final merged congiguration
    """

    """
    Configuration is static

    Disk I/O is expensive

    Prevents reloading on every request
    """

    env = os.getenv("APP_ENV", "dev").lower()

    env_path = os.path.join(CONFIG_DIR, f"{env}.yaml")

    common_config = _read_yaml(COMMON_CONFIG_DIR)
    env_config = _read_yaml(env_path)

    return _deep_merge(common_config, env_config)

def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively merge two dictionaries.

    Args:
        base (dict): Base configuration
        override (dict): Environment-specific overrides

    returns: 
        dict: Merged Configuration.
    """
    """
    Why shallow merge is dangerous

    - It overwrites entire sections
    - Causes missing config at runtime
    """

    merged = dict(base)

    for key, value in override.items():
        if(
            key in merged
            and isinstance(merged[key], dict)
            and isinstance(value, dict)
        ):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    
    return merged
    