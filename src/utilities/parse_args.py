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
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help=(
            "force overwrite files that already exist. "
            + "Default False. Only applies to initialize.py"
        ),
    )
    parser.add_argument(
        "-y",
        "--year",
        type=int,
        default=date.today().year,
        help="which year to process. Defaults to year of system time",
    )
    parser.add_argument(
        "-t",
        "--tkinter",
        action="store_true",
        help="launch Tkinter GUI to accept a file input. Only applies to main.py",
    )
    return parser.parse_args()
