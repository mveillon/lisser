from typing import Dict, Any

from src.read_config.get_config import get_config


def config_globals() -> Dict[str, Any]:
    """
    Returns the global variables set in the config file.

    Parameters:
        None

    Returns:
        globals (Dict[str, Any]): a dictionary mapping the names of the
            variables to their values
    """
    return get_config()["globals"]
