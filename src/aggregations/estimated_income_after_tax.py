import pandas as pd
from datetime import datetime

from src.utilities.helpers import monthly_income
from src.utilities.paths import get_year
from src.utilities.column import Column


def estimated_income_after_tax(
    df: pd.DataFrame, monthly_income: float = monthly_income()
) -> float:
    """
    Returns the estimated income over the course of the data in
    the data.

    Parameters:
        df (DataFrame): a Pandas DataFrame
        monthly_income (float): the monthly income over df. Defaults to result of
            monthly income function

    Returns:
        earned (float): how much money was earned
    """
    fmt = "%Y-%m-%d"
    days_this_year = (
        datetime.strptime(f"{get_year()}-12-31", fmt).date()
        - datetime.strptime(f"{get_year()}-01-01", fmt).date()
    ).days
    days_in_data = (df[Column.DATE].max() - df[Column.DATE].min()).days

    return (days_in_data / days_this_year) * monthly_income * 12
