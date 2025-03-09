import pandas as pd

from src.read_config.config_globals import config_globals
from src.utilities.paths import Paths


def zero_income(df: pd.DataFrame) -> None:
    """
    Checks that the user has overwritten their yearly income.

    Parameters:
        df (DataFrame): not used

    Returns:
        None
    """
    if config_globals()["YEARLY_TAKE_HOME_PAY"][str(Paths.get_year())] == 0:
        raise ValueError(
            "Validation error: yearly pay has not been overwritten in base_config.yml"
            + " or config_overwrite.yml"
        )
