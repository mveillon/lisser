from os import listdir
from os.path import splitext, join
import re
from typing import cast

from src.utilities.parse_args import parse_args


def get_year() -> int:
    """
    Returns the year passed to the command on the command line.

    Parameters:
        None

    Returns:
        year (int): the year passed by the user
    """
    return cast(int, parse_args().year)


def this_years_data() -> str:
    """
    Returns the path to this years data.

    Parameters:
        None

    Returns:
        path (str): this year's data
    """
    return join("src", "ui", "static", "data", str(get_year()))


def _first_spreadsheet(parent: str, sheet_name: str) -> str:
    """
    Returns the path to the first spreadsheet with the given name in the given
    directory.
    """
    sheet_regex = re.escape(sheet_name) + r"\.(xlsx|csv|numbers)$"
    try:
        return next(
            join(parent, f)
            for f in listdir(parent)
            if re.match(sheet_regex, f, flags=re.IGNORECASE)
        )
    except StopIteration:
        return join(parent, sheet_name + ".xlsx")


def spending_path() -> str:
    """
    Returns the directory where this year's spending spreadsheet is located.

    Parameters:
        None

    Returns:
        dir (str): where the spreadsheet is located
    """
    return _first_spreadsheet(this_years_data(), "Spending")


def plots_dir() -> str:
    """
    Returns the directory where the plots are located.

    Parameters:
        None

    Returns:
        dir (str): where the plots are located
    """
    return join(this_years_data(), "plots")


def staging_dir() -> str:
    """
    Returns the directory where the .csv spreadsheets are located.

    Parameters:
        None

    Returns:
        dir (str): where the spreadsheets are located
    """
    return join(this_years_data(), "staging")


def get_out_dir(month: str) -> str:
    """
    Generates the output directory for plots for a given month.

    Parameters:
        month (str): the name of the month

    Returns:
        dir (str): the name of the directory the month's plots
            should go in
    """
    return join(plots_dir(), month, "")


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


def untracked_path() -> str:
    """
    Returns the path to the excel sheet of untracked expenses. This sheet
    contains the handful of transactions that were so large they were not
    included in the monthly spreadhseets so as not to completely throw off
    the graphs.

    Parameters:
        None

    Returns:
        path (str): the path to the untracked sheet
    """
    return _first_spreadsheet(this_years_data(), "Untracked")


def aggregation_path() -> str:
    """
    Returns the path to the aggregation file.

    Parameters:
        None

    Returns:
        path (str): the path to the agg file
    """
    return join(this_years_data(), "aggregation.yml")


def config_path() -> str:
    """
    Returns the path to the config file.

    Parameters:
        None

    Returns:
        path (str): the path to the config file
    """
    return "config_overwrite.yml"


def base_config() -> str:
    """
    Returns the path to the base_config.

    Parameters:
        None

    Returns:
        path (str): the path to base_config.yml
    """
    return "base_config.yml"
