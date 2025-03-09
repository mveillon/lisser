import pandas as pd
from datetime import datetime
from typing import cast

from src.utilities.helpers import monthly_income
from src.utilities.paths import Paths
from src.utilities.column import Column
from src.utilities.day_counts import DayCounts


def estimated_income_after_tax(df: pd.DataFrame) -> float:
    """
    Returns the estimated income over the course of the data in
    the data.

    Parameters:
        df (DataFrame): a Pandas DataFrame

    Returns:
        earned (float): how much money was earned
    """
    fmt = "%m/%d/%Y"
    days_this_year = (
        datetime.strptime(f"12/31/{Paths.get_year()}", fmt).date()
        - datetime.strptime(f"1/1/{Paths.get_year()}", fmt).date()
    ).days
    days_in_data = (df[Column.DATE].max() - df[Column.DATE].min()).days

    return (
        cast(float, days_in_data / days_this_year)
        * monthly_income()
        * DayCounts.months_per_year()
    )
