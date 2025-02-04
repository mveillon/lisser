import pandas as pd
from typing import List
from datetime import datetime, timedelta, date

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
    date_limits = tuple(
        map(lambda d: d.date(), (df[Column.DATE].min(), df[Column.DATE].max()))
    )
    all_dates = get_weeks(*date_limits)
    month_starts, month_dfs = group_by_month(df)

    filt_cond = (df[Column.CATEGORY] == "Bills") & (
        df[Column.PRICE] >= config_globals()["PROJECTED_SPENDING_BILL_THRESHOLD"]
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
            avgs.append(
                ((week_df[Column.PRICE].sum() / one_week.days) * (365 / 12))
                + (
                    monthly_bills[mo][Column.PRICE].sum()
                    * (
                        (365 / 12)
                        / (
                            date(
                                dtm.year + int(dtm.month == 12), (dtm.month % 12) + 1, 1
                            )
                            - timedelta(days=1)
                        ).day
                    )
                )
            )

    return avgs
