from os.path import join

from src.read_data.read_data import read_data
from src.models.paths import Paths
from src.utilities.get_funcs_from_module import (
    get_funcs_from_module,
    get_modules_from_folder,
)


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
        df = read_data(Paths.spending_path())

        for mod in get_modules_from_folder(join("src", "read_data", "validations")):
            for func in get_funcs_from_module(mod):
                func(df)
