import locale
import pandas as pd
from os.path import join
from typing import List, cast, Dict
from datetime import timedelta, date
import json

from src.utilities.read_data import read_data
from src.utilities.paths import staging_dir, get_year, spending_path
from src.utilities.column import Column
from src.read_config.config_globals import config_globals
from src.utilities.types import Number


def monthly_income() -> float:
    """
    Returns the monthly income this year.

    Parameters:
        None

    Returns:
        income (float): how much income was made each month
    """
    return cast(float, config_globals()["YEARLY_TAKE_HOME_PAY"][str(get_year())]) / 12


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
    all_dates = [date(min_day.year, min_day.month, min(min_day.day, 28))]

    while all_dates[-1] < max_day:
        new_year = int(all_dates[-1].month == 12)
        all_dates.append(
            date(
                all_dates[-1].year + new_year,
                all_dates[-1].month + 1 - 12 * new_year,
                all_dates[-1].day,
            )
        )

    return all_dates[:-1]


def find_big_bills() -> None:
    """
    Generates a JSON with all big bills using the spreadsheet in
    `src.utilities.spending_dir()`, writing the result to
    `src.utilities.staging_dir()`.

    Parameters:
        None

    Returns:
        None
    """
    res: Dict[str, Dict[str, Number]] = {}
    df = read_data(spending_path())
    big_bills = df.loc[
        (df[Column.PRICE] >= config_globals()["PROJECTED_SPENDING_BILL_THRESHOLD"])
        & (df[Column.CATEGORY] == "Bills")
    ]
    for _, bill in big_bills.reset_index().iterrows():
        month = bill[Column.DATE].strftime("%B")
        if month in res:
            res[month][bill[Column.TRANSACTION_ID]] = bill[Column.PRICE]
        else:
            res[month] = {bill[Column.TRANSACTION_ID]: bill[Column.PRICE]}

    with open(join(staging_dir(), "bills.json"), "w") as out:
        json.dump(res, out)


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
