import numpy as np
import pandas as pd
from pandas.api.types import is_string_dtype
from os.path import splitext

from functools import lru_cache
from uuid import uuid4
from numbers_parser import Document
from typing import List, cast, Dict

from src.utilities.column import Column
from src.utilities.paths import spending_path
from src.read_config.config_globals import config_globals


SCHEMA = {
    Column.DATE: "str",
    Column.VENDOR: "str",
    Column.CATEGORY: "str",
    Column.PRICE: "float",
    Column.IS_FOOD: "int",
    Column.CONTROLLABLE: "int",
    Column.TRANSACTION_ID: "str",
}


@lru_cache(maxsize=16)
def read_data(path: str) -> pd.DataFrame:
    """
    Reads the data and converts any columns that need converting. Can read
    many different file types.

    Parameters:
        path (str): the path of the spreadsheet

    Returns:
        df (DataFrame): a Pandas DataFrame with the spreadsheet info
    """
    readers = {
        ".txt": _read_csv,
        ".csv": _read_csv,
        ".numbers": _read_numbers,
        ".xlsx": _read_excel,
    }
    df = readers[splitext(path)[1]](path)

    new_cols: Dict[str, np.ndarray] = {
        Column.TRANSACTION_ID: np.fromiter(
            map(lambda _: str(uuid4()), np.empty(df.shape[0])),
            count=df.shape[0],
            dtype=np.dtypes.StringDType(),
        )
    }
    if is_string_dtype(df[Column.PRICE]):
        new_cols[Column.PRICE] = np.array(
            df[Column.PRICE].str.replace(
                r"[^\d\-.]",
                "",
                regex=True,
            )
        )

    df = df.assign(**new_cols)
    for col_name, dtype in SCHEMA.items():
        df[col_name] = df[col_name].astype(cast(pd.BooleanDtype, dtype))

    df[Column.IS_FOOD] = df[Column.IS_FOOD].astype("boolean")
    df[Column.CONTROLLABLE] = df[Column.CONTROLLABLE].astype("boolean")
    df[Column.DATE] = pd.to_datetime(
        df[Column.DATE], format="mixed", dayfirst=False, yearfirst=False
    )

    return df

def filter_large_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Throws out outlier transactions that throw off certain calculations.

    Parameters:
        df (DataFrame): the Pandas DataFrame to filter

    Returns:
        df (DataFrame): the filtered DataFrame
    """
    return df.loc[df[Column.PRICE] < config_globals()["LARGE_EXPENSE_THRESHOLD"]]

def _read_excel(path: str) -> pd.DataFrame:
    """
    Reads an excel file and turns it into an unprocessed DataFrame.
    """
    return pd.read_excel(
        path,
        sheet_name="Sheet1",
        header=0,
    )


def _read_csv(path: str) -> pd.DataFrame:
    """
    Reads a csv file and turns it into an unprocessed DataFrame.
    """
    return pd.read_csv(path, header=0, encoding="ISO-8859-1")


def _read_numbers(path: str) -> pd.DataFrame:
    """
    Reads a numbers file and turns it into an unprocessed DataFrame.
    """
    data = Document(path).sheets[0].tables[0].rows(values_only=True)
    return pd.DataFrame(data[1:], columns=data[0])


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
