from os import listdir
from os.path import splitext, join, basename
from typing import cast, List
from datetime import datetime

from src.utilities.parse_args import parse_args, Subcommand
from src.read_data.read_data import read_data
from src.read_data.column import Column


ALLOWED_EXTNS = {
    ".xlsx",
    ".csv",
    ".numbers",
    ".txt",
}


def _default_year() -> int:
    """
    Returns the year passed to the command on the command line, or the
    system time's year if no year was passed.
    """
    cmd = parse_args().subparser_name
    if cmd == Subcommand.CLI and parse_args().file is not None:
        return cast(datetime, read_data(parse_args().file)[Column.DATE].median()).year

    if cmd in (Subcommand.CLI, Subcommand.INIT):
        return cast(int, parse_args().year)

    return datetime.now().year


def _first_spreadsheet(parent: str, sheet_name: str) -> str:
    """
    Returns the path to the first spreadsheet with the given name in the given
    directory.
    """
    try:
        return next(
            join(parent, f)
            for f in listdir(parent)
            if splitext(basename(f))[0] == sheet_name
            and splitext(f)[1] in ALLOWED_EXTNS
        )
    except StopIteration:
        return join(parent, sheet_name + ".xlsx")


class Paths:
    _year_mut: List[int] = [_default_year()]
    _sheet_override: List[str] = [""]

    @staticmethod
    def get_year() -> int:
        """
        Returns the year passed to the command on the command line, or the
        system time's year if no year was passed.

        Parameters:
            None

        Returns:
            year (int): which year to analyze
        """
        return Paths._year_mut[0]

    @staticmethod
    def this_years_data() -> str:
        """
        Returns the path to this years data.

        Parameters:
            None

        Returns:
            path (str): this year's data
        """
        return join("data", str(Paths.get_year()))

    @staticmethod
    def spending_path() -> str:
        """
        Returns the directory where this year's spending spreadsheet is located.

        Parameters:
            None

        Returns:
            dir (str): where the spreadsheet is located
        """
        if len(Paths._sheet_override[0]) > 0:
            return Paths._sheet_override[0]

        if (
            parse_args().subparser_name == Subcommand.CLI
            and parse_args().file is not None
        ):
            return parse_args().file

        return _first_spreadsheet(Paths.this_years_data(), "Spending")

    @staticmethod
    def plots_dir() -> str:
        """
        Returns the directory where the plots are located.

        Parameters:
            None

        Returns:
            dir (str): where the plots are located
        """
        return join(Paths.this_years_data(), "plots")

    @staticmethod
    def get_out_dir(month: str) -> str:
        """
        Generates the output directory for plots for a given month.

        Parameters:
            month (str): the name of the month

        Returns:
            dir (str): the name of the directory the month's plots
                should go in
        """
        return join(Paths.plots_dir(), month, "")

    @staticmethod
    def is_excel(path: str) -> bool:
        """
        Checks if the file at `path` is an excel file and that it's
        readable.

        Parameters:
            path (str): the path of the file. Also works with just the filename

        Returns:
            is_excel (bool): whether the file is an excel sheet that should be plotted
        """
        return splitext(path)[1] == ".xlsx" and "~" not in path

    @staticmethod
    def aggregation_path() -> str:
        """
        Returns the path to the aggregation file.

        Parameters:
            None

        Returns:
            path (str): the path to the agg file
        """
        return join(Paths.this_years_data(), "aggregation.csv")

    @staticmethod
    def config_path() -> str:
        """
        Returns the path to the config file.

        Parameters:
            None

        Returns:
            path (str): the path to the config file
        """
        return "config_overwrite.yml"

    @staticmethod
    def base_config() -> str:
        """
        Returns the path to the base_config.

        Parameters:
            None

        Returns:
            path (str): the path to base_config.yml
        """
        return "base_config.yml"
