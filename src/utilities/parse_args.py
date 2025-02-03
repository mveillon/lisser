from datetime import date
import argparse
from functools import lru_cache

from typing import Callable
from enum import StrEnum


class Subcommand(StrEnum):
    CLI = "cli"
    UI = "ui"
    INIT = "init"
    UNSET = "unset"


_SELECTED_SUB = Subcommand.UNSET


def get_subcommand() -> Subcommand:
    """
    Returns which subcommand was selected on the command line.

    Parameters:
        None

    Returns:
        None
    """
    return _SELECTED_SUB


def set_command(sub: Subcommand) -> Callable[[], None]:
    """
    Returns a function which sets the subcommand returned by `get_subcommand`.

    Parameters:
        sub (Subparser): which subparser was selected

    Returns:
        callback (Callable[[], None]): a function to call to set the subparser to `sub`
    """
    def res() -> None:
        global _SELECTED_SUB
        _SELECTED_SUB = sub

    return res


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
    subparsers = parser.add_subparsers(
        title="subcommands",
        description="valid subcommands",
        help="which command to run",
    )

    cli_parser = subparsers.add_parser(Subcommand.CLI, help="cli help")
    ui_parser = subparsers.add_parser(Subcommand.UI, help="ui help")
    init_parser = subparsers.add_parser(Subcommand.INIT, help="init help")

    year_arg = (
        (
            "-y",
            "--year",
        ),
        {
            "type": int,
            "default": date.today().year,
            "help": "which year to process. Defaults to year of system time",
        },
    )

    cli_parser.add_argument(*year_arg[0], **year_arg[1])  # type: ignore
    init_parser.add_argument(*year_arg[0], **year_arg[1])  # type: ignore

    init_parser.add_argument(
        "-F",
        "--force",
        action="store_true",
        help=(
            "force overwrite files that already exist. "
            + "Default False. Only applies to initialize.py"
        ),
    )

    cli_parser.add_argument(
        "-f",
        "--file",
        default="",
        help=(
            "the path of the file to process. "
            + "Defaults to /data/{year}/Spending.{xlsx|csv|txt|numbers}"
        ),
    )

    cli_parser.set_defaults(func=set_command(Subcommand.CLI))
    ui_parser.set_defaults(func=set_command(Subcommand.UI))
    init_parser.set_defaults(func=set_command(Subcommand.INIT))

    return parser.parse_args()
