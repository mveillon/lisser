import yaml
from functools import lru_cache

from typing import Dict, Any

from src.utilities.paths import config_path


@lru_cache(maxsize=1)
def config_globals() -> Dict[str, Any]:
    """
    Returns the global variables set in the config file.

    Params:
        None

    Returns:
        globals (Dict[str, Any]): a dictionary mapping the names of the
            variables to their values
    """
    with open(config_path(), "r") as c:
        data = yaml.safe_load(c)

    return data["globals"]
