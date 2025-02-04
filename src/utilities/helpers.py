import locale
import pandas as pd
from typing import List, cast
from datetime import timedelta, date

from src.utilities.paths import Paths
from src.utilities.column import Column
from src.read_config.config_globals import config_globals


def monthly_income() -> float:
    """
    Returns the monthly income this year.

    Parameters:
        None

    Returns:
        income (float): how much income was made each month
    """
    return (
        cast(float, config_globals()["YEARLY_TAKE_HOME_PAY"][str(Paths.get_year())])
        / 12
    )


def format_currency(money: float) -> str:
    """
    Formats the currency nicely.

    Parameters:
        money (float): the amount of money

    Returns:
        formatted (str): the same number formatted into a
            currency string
    """
    locale.setlocale(locale.LC_ALL, "")
    return locale.currency(money, grouping=True)


def get_weeks(min_day: date, max_day: date) -> List[date]:
    """
    Generates the first day of every week between `min_day` and `max_day`,
    both inclusive.

    Parameters:
        min_day (date): the first day in the range
        max_day (date): the last day in the range

    Returns:
        weeks (List[date]): starting with `min_day`, generates a list
            of the first day each week until and possibly including
            `max_day`
    """
    one_week = timedelta(weeks=1)
    all_dates = [min_day]

    while all_dates[-1] < max_day:
        all_dates.append(all_dates[-1] + one_week)

    return all_dates[:-1]


def get_months(min_day: date, max_day: date) -> List[date]:
    """
    Generates the first day of every month between `min_day` and `max_day`,
    both inclusive.

    Parameters:
        min_day (date): the first day in the range
        max_day (date): the last day in the range

    Returns:
        months (List[date]): starting with `min_day`, generates a list
            of the first day each month until and possibly including
            `max_day`
    """
    all_dates = [date(min_day.year, min_day.month, 1)]

    while all_dates[-1] <= max_day:
        all_dates.append(
            date(
                all_dates[-1].year + int(all_dates[-1].month == 12),
                (all_dates[-1].month % 12) + 1,
                1,
            )
        )

    return all_dates[:-1]


def time_filter(df: pd.DataFrame, min_date: str, max_date: str) -> pd.DataFrame:
    """
    Finds purchases made between min_date and max_date and
    returns the filtered Dataframe.
    e.g. `time_filter(df, '1/2/24', '1/6/24')`

    Parameters:
        df (DataFrame): the Pandas DataFrame to filter
        min_date (str): the minimum date to look for
        max_date (str): the maximum date to look for

    Returns:
        df (DataFrame): `df` filtered to be between `min_date` and `max_date`
    """
    return df.loc[(df[Column.DATE] >= min_date) & (df[Column.DATE] < max_date)]
