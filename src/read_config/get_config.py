import yaml
from functools import lru_cache
import os.path

from src.utilities.paths import Paths
from src.utilities.dictionary_ops import recursive_merge


@lru_cache(maxsize=1)
def get_config() -> dict:
    """
    Returns all user configs.

    Parameters:
        None

    Returns:
        config (dict): a dictionary of all configs defined
            by the user
    """
    with open(Paths.base_config(), "r") as base:
        base_data = yaml.safe_load(base)

    if os.path.exists(Paths.config_path()):
        with open(Paths.config_path(), "r") as prim:
            primary_data = yaml.safe_load(prim)

    else:
        primary_data = {}

    recursive_merge(base_data, primary_data)
    return base_data
