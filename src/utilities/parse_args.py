from datetime import date
import argparse
from functools import lru_cache
from enum import StrEnum


class Subcommand(StrEnum):
    CLI = "cli"
    UI = "ui"
    INIT = "init"
    UNSET = "unset"


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
        dest="subparser_name",
    )

    cli_parser = subparsers.add_parser(Subcommand.CLI, help="run using the CLI")
    _ = subparsers.add_parser(Subcommand.UI, help="launch the Tkinter UI")
    init_parser = subparsers.add_parser(
        Subcommand.INIT, help="initialize the repository"
    )

    for par in (cli_parser, init_parser):
        par.add_argument(
            "-y",
            "--year",
            type=int,
            default=date.today().year,
            help="which year to process. Defaults to year of system time.",
        )

    init_parser.add_argument(
        "-F",
        "--force",
        action="store_true",
        help=("force overwrite files that already exist. Default False."),
    )

    cli_parser.add_argument(
        "-f",
        "--file",
        help=(
            "the path of the file to process. "
            + "Defaults to /data/{year}/Spending.{xlsx|csv|txt|numbers}"
        ),
    )

    return parser.parse_args()
