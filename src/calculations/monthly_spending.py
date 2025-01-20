import pandas as pd
from typing import Dict
from datetime import date

from src.utilities.helpers import time_filter
from src.utilities.column import Column

from src.calculations.projected_spending import projected_spending


def monthly_spending(df: pd.DataFrame) -> Dict[str, float]:
    """
    Calculates how much was spent each month in df.

    Parameters:
        df (DataFrame): the Pandas DataFrame to analyze

    Returns:
        monthly_spending (Dict[str, float]): mapping from month name to
            how much was spent that month
    """
    current: date = df[Column.DATE].min().date()
    end: date = df[Column.DATE].max().date()
    res = {}
    fmt = "%Y/%m/%d"

    while current <= end:
        if current.month == 12:
            next_date = date(current.year + 1, current.month, current.day)
        else:
            next_date = date(current.year, current.month + 1, current.day)

        month_df = time_filter(df, current.strftime(fmt), next_date.strftime(fmt))
        month_str = current.strftime("%B")
        if next_date > end:
            spent = projected_spending(df, month_str, filter_big_bills=False)
        else:
            spent = month_df[Column.PRICE].sum()

        res[current.strftime("%b")] = spent
        current = next_date

    return res
