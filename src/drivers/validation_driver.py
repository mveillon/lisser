from os import makedirs
from os.path import join, exists

from src.read_data.read_data import read_data
from src.models.paths import Paths
from src.utilities.get_funcs_from_module import (
    get_funcs_from_module,
    get_modules_from_folder,
)
from src.initialize import add_spending_sheet


class ValidationDriver:
    """
    Class to handle all validations on the user spreadsheet.
    """

    def validate_spending(self) -> None:
        """
        Validates the spending spreadsheet, performing all checks in the `validations`
        directory.

        Parameters:
            None

        Returns:
            None
        """
        makedirs(Paths.this_years_data(), exist_ok=True)
        if not exists(Paths.spending_path()):
            add_spending_sheet()

        df = read_data(Paths.spending_path())

        for mod in get_modules_from_folder(join("src", "read_data", "validations")):
            for func in get_funcs_from_module(mod):
                func(df)
