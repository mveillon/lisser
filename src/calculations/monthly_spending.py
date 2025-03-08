import numpy as np
import pandas as pd
from typing import Dict
from datetime import date, timedelta

from src.utilities.day_counts import DayCounts
from src.utilities.helpers import time_filter
from src.utilities.column import Column
from src.read_config.config_globals import config_globals


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
    fmt = "%m/%d/%Y"

    while current <= end:
        next_date = date(
            current.year + int(current.month == DayCounts.months_per_year()),
            (current.month % DayCounts.months_per_year()) + 1,
            1,
        ) - timedelta(days=1)

        month_df = time_filter(df, current.strftime(fmt), next_date.strftime(fmt))

        thresh = config_globals()["PROJECTED_SPENDING_BILL_THRESHOLD"]
        filt_cond = (df[Column.CATEGORY] == "Bills") & (
            df[Column.PRICE] >= (thresh if thresh >= 0 else np.inf)
        )

        bills = month_df.loc[filt_cond][Column.PRICE].sum()
        month_df = month_df.loc[~filt_cond]

        num_days = (month_df[Column.DATE].max() - month_df[Column.DATE].min()).days
        spent = (month_df[Column.PRICE].sum() / num_days) * DayCounts.days_per_month()
        spent += (bills / (next_date - current).days) * DayCounts.days_per_month()

        res[current.strftime("%b")] = spent
        current = next_date + timedelta(days=1)

    return res
