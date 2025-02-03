import pandas as pd
from os.path import join
import json

from src.utilities.paths import Paths
from src.utilities.column import Column


def projected_spending(
    df: pd.DataFrame,
    month: str,
    total_days: int = 0,
    filter_big_bills: bool = True,
) -> float:
    """
    Average spent per 30 days, spreading out large bills that occur at the start
    of the month if `filter_big_bills` is True. Goal is to be less than
    $6,000 or so.

    Arguments:
      df (pd.Dataframe): the source Dataframe. Typically filtered
        using `time_filter`
      month (str): the month to source the big bills from. Should be
        either 'Combined' or contained in bills.json
      total_days (int): the number of days the spending spans. If zero,
        the default, the time period will be calculated using the
        `Date` field of `df`
      filter_big_bills (bool): whether or not to filter out the
        large bills at the beginning of the month and spread them across
        other weeks.

    Returns:
      per_month (float): a projection of how much would be spent over a
        full month at the pace given in `df`
    """
    total_spent = df[Column.PRICE].sum()
    if total_days == 0:
        total_days = (df[Column.DATE].max() - df[Column.DATE].min()).days

    bills_total = 0
    if filter_big_bills:
        with open(join(Paths.staging_dir(), "bills.json")) as bills:
            data = json.load(bills)
            for bill_id in data.get(month, {}):
                total_spent -= df.loc[df[Column.TRANSACTION_ID] == bill_id][
                    Column.PRICE
                ].sum()
                bills_total += data[month][bill_id]

    res = (total_spent / total_days) * (365 / 12) if total_days > 0 else 0
    res += bills_total
    return res
