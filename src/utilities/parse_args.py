from datetime import date
import argparse
from functools import lru_cache


@lru_cache(maxsize=1)
def parse_args() -> argparse.Namespace:
    """
    Returns the command line arguments.

    Parameters:
        None

    Returns:
        args (Dict[str, str]): the command line arguments
    """
    parser = argparse.ArgumentParser(
        prog="spending_tracking",
        description="Initialize repository.",
    )
    parser.add_argument("-f", "--force", action="store_true")
    parser.add_argument("-y", "--year", type=int, default=date.today().year)
    return parser.parse_args()
