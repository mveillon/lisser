import yaml
from functools import lru_cache
import os.path

from typing import Dict, Any

from src.utilities.paths import base_config, config_path
from src.utilities.dictionary_ops import recursive_merge


@lru_cache(maxsize=1)
def get_config() -> Dict[str, Any]:
    """
    Returns all user configs.

    Parameters:
        None

    Returns:
        config (dict): a dictionary of all configs defined
            by the user
    """
    with open(base_config(), "r") as base:
        base_data = yaml.safe_load(base)

    if os.path.exists(config_path()):
        with open(config_path(), "r") as prim:
            primary_data = yaml.safe_load(prim)

    else:
        primary_data = {}

    recursive_merge(base_data, primary_data)
    return base_data
