import shutil
from os.path import exists
from os import makedirs

from src.utilities.paths import (
    config_path,
    spending_path,
    this_years_data,
)
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
        parse_args().force
        or not exists(dest)
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


def init_config():
    """
    Initialize the config_overwrite.yml file.

    Parameters:
        None

    Returns:
        None
    """
    dest = config_path()

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


def add_spending_sheet():
    """
    Creates the base of the spending directory.

    Parameters:
        None

    Returns:
        None
    """
    makedirs(this_years_data(), exist_ok=True)

    spending = spending_path()
    if check_overwrite(spending):
        shutil.copy("base_sheet.xlsx", spending)


if __name__ == "__main__":
    init_config()
    add_spending_sheet()
