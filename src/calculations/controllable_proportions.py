import pandas as pd
from typing import Tuple

from src.models.day_counts import DayCounts
from src.utilities.helpers import monthly_income
from src.read_data.column import Column


def controllable_proportions(df: pd.DataFrame) -> Tuple[float, float, float]:
    """
    Returns how much spent money is controllable and how much isn't, as well
    as the total income over that period.

    Parameters:
        df (DataFrame): the Pandas DataFrame to analyze

    Returns:
        controllable (float): how much is controllable
        not_controllable (float): how much is not controllable
        total_income (float): how much money was made in that period
    """
    control_sum = df.loc[df[Column.CONTROLLABLE]][Column.PRICE].sum()
    not_control_sum = df.loc[~df[Column.CONTROLLABLE]][Column.PRICE].sum()

    total_days = (df[Column.DATE].max() - df[Column.DATE].min()).days
    total_income = total_days * monthly_income() / DayCounts.days_per_month()
    return control_sum, not_control_sum, total_income
