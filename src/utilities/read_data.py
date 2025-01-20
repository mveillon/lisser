import pandas as pd
from datetime import datetime, date
from functools import lru_cache
from typing import List

from src.utilities.column import Column
from src.utilities.parse_args import parse_args
from src.utilities.paths import spending_path


@lru_cache(maxsize=16)
def read_data(path: str) -> pd.DataFrame:
    """
    Reads the data and converts any columns that need converting.

    Parameters:
        path (str): the path of the *.xlsx file

    Returns:
        df (DataFrame): a Pandas DataFrame with the spreadsheet info
    """
    df = pd.read_excel(
        path,
        sheet_name="Sheet1",
        header=0,
        usecols=list(Column),
        dtype={
            Column.DATE: "str",
            Column.DESCRIPTION: "str",
            Column.VENDOR: "str",
            Column.CATEGORY: "str",
            Column.PRICE: "float",
            Column.IS_FOOD: "int",
            Column.CONTROLLABLE: "int",
        },
    )
    df[Column.DATE] = pd.to_datetime(df[Column.DATE], format="%Y-%m-%d %H:%M:%S")
    df[Column.IS_FOOD] = df[Column.IS_FOOD].astype("boolean")
    df[Column.CONTROLLABLE] = df[Column.CONTROLLABLE].astype("boolean")

    if df.shape[0] == 0:
        return pd.DataFrame(
            [[datetime(parse_args().year, 1, 1), "", "", "", 0.0, False, False]],
            columns=df.columns,
        )

    return df


def combined_df() -> pd.DataFrame:
    """
    Returns a single DataFrame with all spreadsheets combined.

    Parameters:
        root (str): the root directory of the input files

    Returns:
        df (DataFrame): a Pandas DataFrame with the data of
            all the spreadsheets
    """
    return read_data(spending_path())


def get_months(year_data: pd.DataFrame) -> List[pd.DataFrame]:
    """
    Returns the transactions partitioned into months.

    Parameters:
        year_data (DataFrame): the full year of data

    Returns:
        months (List[DataFrame]): the data partitioned into months
    """
    groups = year_data.groupby(pd.Grouper(key=Column.DATE, freq="ME"))
    return [df for _, df in groups]


def month_to_df(month: str) -> pd.DataFrame:
    """
    Reads and filters the data to just transactions in the given
    month.

    Parameters:
        month (str): which month to filter. Should be '%B' format,
            e.g. January, March

    Returns:
        data (DataFrame): the month of data
    """
    mo = int(datetime.strftime(month, "%B").strptime("%m"))
    full = combined_df()
    yr = round(full[Column.DATE].mean())
    return full.loc[
        (full[Column.DATE] >= date(yr, mo, 1))
        & (full[Column.DATE] < date(yr + int(mo == 12), (mo % 12) + 1, 1))
    ]
