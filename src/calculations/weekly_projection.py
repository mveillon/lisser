import pandas as pd
from typing import List
from datetime import datetime, timedelta, time

from src.utilities.helpers import get_weeks, time_filter, get_months
from src.utilities.column import Column
from src.read_config.config_globals import config_globals


def weekly_projection(df: pd.DataFrame) -> List[float]:
    """
    Finds the monthly spending projection for each week.

    Parameters:
        df (DataFrame): the Pandas DataFrame to analyze

    Returns:
        week_spent (List[float]): how much was spent per week,
            projected as a per_month total
    """
    fmt = "%m/%d/%Y"
    one_week = timedelta(weeks=1)
    date_limits = tuple(map(lambda d: d.date(), (df[Column.DATE].min(), df[Column.DATE].max())))
    all_dates = get_weeks(*date_limits)
    all_months = get_months(*date_limits)

    monthly_bills = []
    filt_cond = (df[Column.CATEGORY] == "Bills") & (
        df[Column.PRICE] >= config_globals()["PROJECTED_SPENDING_BILL_THRESHOLD"]
    )
    fmt = "%m/%d/%Y"
    for i, month_start in enumerate(all_months):
        monthly_bills.append(
            time_filter(
                df,
                month_start.strftime(fmt),
                (
                    all_months[i + 1] if i < len(all_months) - 1 else datetime.max
                ).strftime(fmt),
            )
            .loc[filt_cond][Column.PRICE]
            .sum()
        )
    df = df.loc[~filt_cond]

    avgs = []
    for i in range(len(all_dates)):
        dtm = datetime.combine(all_dates[i], datetime.min.time())
        week_df = time_filter(
            df,
            datetime.strftime(dtm, fmt),
            datetime.strftime(dtm + one_week, fmt),
        )

        if week_df.shape[0] > 0:
            avgs.append(0.0)
        else:
            avgs.append(week_df[Column.PRICE].sum() * (365 / 12) / one_week.days)

    return avgs
