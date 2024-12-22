import pandas as pd
from typing import Tuple

from src.calculations.controllable_proportions import controllable_proportions


def expenses_split(df: pd.DataFrame) -> Tuple[float, float, float]:
    """
    Returns what percentage of expenses were not controllable, controllable,
    and how much was put into savings. Should be about 50/30/20 because
    the economy is shit.

    Parameters:
        df (DataFrame): the Pandas DataFrame to analyze

    Returns:
        not_controllable (float): how much was not controllable
        controllable (float): how much was controllable
        saved (float): how much was saved
    """
    control, not_control, income = controllable_proportions(df)
    to_perc = lambda f: round(100 * f, 2)
    if income == 0:
        return 0, 0, 0
    return (
        to_perc(not_control / income),
        to_perc(control / income),
        to_perc((income - (control + not_control)) / income),
    )
