import pandas as pd
from typing import Tuple

from src.calculations.controllable_proportions import controllable_proportions
from src.utilities.helpers import monthly_income


def expenses_split(
    df: pd.DataFrame, monthly_income: float = monthly_income()
) -> Tuple[float, float, float]:
    """
    Returns what percentage of expenses were not controllable, controllable,
    and how much was put into savings. Should be about 50/30/20 because
    the economy is shit.

    Parameters:
        df (DataFrame): the Pandas DataFrame to analyze
        monthly_income (float): the monthly income over df. Defaults to result of
            monthly income function

    Returns:
        not_controllable (float): how much was not controllable
        controllable (float): how much was controllable
        saved (float): how much was saved
    """
    control, not_control, income = controllable_proportions(
        df, monthly_income=monthly_income,
    )
    to_perc = lambda f: round(100 * f, 2)
    if income == 0:
        return 0, 0, 0
    return (
        to_perc(not_control / income),
        to_perc(control / income),
        to_perc((income - (control + not_control)) / income),
    )
