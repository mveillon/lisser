import pandas as pd
from os import listdir
from os.path import join, basename
import subprocess
from datetime import datetime

from src.utilities.paths import staging_dir, month_from_path, is_excel, untracked_path
from src.utilities.column import Column
from src.utilities.parse_args import parse_args


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
        # usecols=[*Column],
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


def _read_numbers(path: str) -> pd.DataFrame:
    """
    Reads the data from the .numbers file and converts any columns that
    need converting. Kept only for historical reasons.

    Parameters:
        path (str): the path of the *.numbers file

    Returns:
        df (DataFrame): a Pandas DataFrame with the spreadsheet info
    """
    csv_path = join(staging_dir(), month_from_path(path) + ".csv")
    subprocess.Popen(f"cat-numbers -b {path} > {csv_path}", shell=True).wait()

    df = pd.read_csv(
        csv_path,
        header=0,
        dtype={
            Column.DATE: "str",
            Column.DESCRIPTION: "str",
            Column.VENDOR: "str",
            Column.CATEGORY: "str",
            Column.PRICE: "float",
            Column.IS_FOOD: "boolean",
            Column.CONTROLLABLE: "boolean",
        },
    )
    df[Column.DATE] = pd.to_datetime(df[Column.DATE], format="%Y-%m-%d %H:%M:%S%z")
    return df


def combined_df(root: str) -> pd.DataFrame:
    """
    Returns a single DataFrame with all spreadsheets combined.

    Parameters:
        root (str): the root directory of the input files

    Returns:
        df (DataFrame): a Pandas DataFrame with the data of
            all the spreadsheets
    """
    dfs = []
    for path in listdir(root):
        if is_excel(path) and basename(path) != basename(untracked_path()):
            dfs.append(read_data(join(root, path)))

    return pd.concat(dfs)
