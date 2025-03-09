import numpy as np
import pandas as pd
from typing import List
from datetime import datetime, timedelta, date

from src.utilities.day_counts import DayCounts
from src.utilities.helpers import get_weeks, time_filter
from src.utilities.column import Column
from src.read_config.config_globals import config_globals
from src.utilities.df_common import group_by_month


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
    all_dates = get_weeks(df[Column.DATE].min().date(), df[Column.DATE].max().date())
    month_starts, month_dfs = group_by_month(df)

    thresh = config_globals()["PROJECTED_SPENDING_BILL_THRESHOLD"]
    filt_cond = (df[Column.CATEGORY] == "Bills") & (
        df[Column.PRICE] >= (thresh if thresh > 0 else np.inf)
    )

    monthly_bills = {}
    for month_dtm, sub_df in zip(month_starts, month_dfs):
        monthly_bills[month_dtm.strftime("%B")] = sub_df.loc[filt_cond]

    df = df.loc[~filt_cond]

    fmt = "%m/%d/%Y"
    avgs = []
    for i in range(len(all_dates)):
        dtm = datetime.combine(all_dates[i], datetime.min.time())
        week_df = time_filter(
            df,
            datetime.strftime(dtm, fmt),
            datetime.strftime(dtm + one_week, fmt),
        )

        mo = dtm.strftime("%B")
        if mo in monthly_bills:
            week_df = week_df.loc[
                ~week_df[Column.TRANSACTION_ID].isin(
                    list(monthly_bills[mo][Column.TRANSACTION_ID])
                )
            ]

        if week_df.shape[0] == 0:
            avgs.append(0.0)
        else:
            monthly_bill_smooth = monthly_bills[mo][Column.PRICE].sum() * (
                DayCounts.days_per_month()
                / (
                    date(
                        dtm.year + int(dtm.month == DayCounts.months_per_year()),
                        (dtm.month % DayCounts.months_per_year()) + 1,
                        1,
                    )
                    - timedelta(days=1)
                ).day
            )

            avgs.append(
                (
                    (week_df[Column.PRICE].sum() / one_week.days)
                    * DayCounts.days_per_month()
                )
                + monthly_bill_smooth
            )

    return avgs
