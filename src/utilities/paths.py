from os.path import splitext, basename, join

from src.utilities.parse_args import parse_args


def get_year() -> int:
    """
    Returns the year passed to the command on the command line.

    Parameters:
        None

    Returns:
        year (int): the year passed by the user
    """
    return parse_args().year


def this_years_data() -> str:
    """
    Returns the path to this years data.

    Parameters:
        None

    Returns:
        path (str): this year's data
    """
    return join("data", str(get_year()))


def sheet_dir() -> str:
    """
    Returns the directory where the .numbers spreadsheets are located.

    Parameters:
        None

    Returns:
        dir (str): where the spreadsheets are located
    """
    return join(this_years_data(), "spending")


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


def month_from_path(path: str) -> str:
    """
    Parses the path to find the name of the month. Assumes the spreadsheet
    is named {{month}}.numbers or {{month}}.xlsx.

    Parameters:
        path (str): the potentially absolute path of the spreadsheet
            with the month name in it

    Returns:
        month (str): the name of the month of the spreadsheet
    """
    if path[-1] == "/":
        path = path[:-1]
    return splitext(basename(path))[0]


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
    return join(sheet_dir(), "Untracked.xlsx")


def aggregation_path() -> str:
    """
    Returns the path to the aggregation file.

    Parameters:
        None

    Returns:
        path (str): the path to the agg file
    """
    return join(this_years_data(), "aggregation.yml")


def income_path() -> str:
    """
    Returns the path to the income file.

    Parameters:
        None

    Returns:
        path (str): the path to the income file
    """
    return join(this_years_data(), "income.txt")


def config_path() -> str:
    """
    Returns the path to the config file.

    Paramters:
        None

    Returns:
        path (str): the path to the config file
    """
    return "config.yml"
