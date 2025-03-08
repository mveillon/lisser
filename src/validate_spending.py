from pathlib import Path

from src.utilities.read_data import read_data
from src.utilities.paths import Paths
from src.utilities.get_funcs_from_module import get_funcs_from_module, get_modules_from_folder


def validate_spending() -> None:
    """
    Validates the spending spreadsheet, performing all checks in the `validations`
    directory.

    Parameters:
        None

    Returns:
        None
    """
    df = read_data(Paths.spending_path())

    for mod in get_modules_from_folder(str(Path(__file__).parent / "validations")):
        for func in get_funcs_from_module(mod):
            func(df)
