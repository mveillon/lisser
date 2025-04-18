import shutil
from os.path import exists
from os import makedirs

from src.models.paths import Paths
from src.utilities.parse_args import parse_args


def check_overwrite(dest: str) -> bool:
    """
    Checks with the user on the CLI before overwriting files,
    unless the --force option is enabled.

    Parameters:
        dest (str): the destination path

    Returns:
        allowed (bool): whether the overwrite is approved
    """
    return (
        not exists(dest)
        or parse_args().force
        or (
            input(
                f"This will overwrite existing the data at {dest}. "
                + "Do you want to continue? (y/N)"
            )
            .lower()
            .strip()
            in ("y", "yes")
        )
    )


def init_config() -> None:
    """
    Initialize the config_overwrite.yml file.

    Parameters:
        None

    Returns:
        None
    """
    dest = Paths.config_path()

    if check_overwrite(dest):
        with open(dest, "w") as out:
            out.write(
                "\n\n".join(
                    (
                        "globals: {}",
                        "plots: {}",
                        "aggregations: {}",
                    )
                )
            )


def add_spending_sheet() -> None:
    """
    Creates the base of the spending directory.

    Parameters:
        None

    Returns:
        None
    """
    makedirs(Paths.this_years_data(), exist_ok=True)

    spending = Paths.spending_path()
    if check_overwrite(spending):
        shutil.copy("base_sheet.xlsx", spending)


def initialize() -> None:
    """
    Performs all necessary initializations.
    """
    init_config()
    add_spending_sheet()
