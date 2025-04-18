import numpy as np
import pandas as pd
from pandas.api.types import is_string_dtype
from os.path import splitext

from functools import lru_cache
from uuid import uuid4
from numbers_parser import Document
from typing import List, cast, Dict

from src.read_data.column import Column


SCHEMA = {
    Column.DATE: "str",
    Column.CATEGORY: "str",
    Column.PRICE: "float",
    Column.IS_FOOD: "int",
    Column.CONTROLLABLE: "int",
    Column.TRANSACTION_ID: "str",
}


@lru_cache(maxsize=32)
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
    df = df.loc[~df[Column.DATE].isna()]

    new_cols: Dict[str, np.ndarray] = {
        Column.TRANSACTION_ID: np.fromiter(
            [str(uuid4()) for _ in range(df.shape[0])],
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


def get_month_dfs(year_data: pd.DataFrame) -> List[pd.DataFrame]:
    """
    Returns the transactions partitioned into months.

    Parameters:
        year_data (DataFrame): the full year of data

    Returns:
        months (List[DataFrame]): the data partitioned into months
    """
    groups = year_data.groupby(pd.Grouper(key=Column.DATE, freq="ME"))
    return [df for _, df in groups if df.shape[0]]
