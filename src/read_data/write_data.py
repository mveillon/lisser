import pandas as pd
from os.path import basename, splitext
from typing import Literal

from src.read_data.column import Column


def write_data(df: pd.DataFrame, path: str, mode: Literal["w", "a", "x"] = "w") -> None:
    """
    Writes the DataFrame to the given path, handling multiple
    kinds of spreadsheet.

    Parameters:
        df (DataFrame): the DataFrame to write
        path (str): where to write to
        mode (str): the write mode. Default is "w", and can also be "a" or "x"

    Returns:
        None
    """
    writers = {
        ".xlsx": _write_excel,
        ".numbers": _write_numbers,
        ".csv": _write_csv,
        ".txt": _write_csv,
    }
    extn = splitext(basename(path))[1]
    writers[extn](df, path, mode=mode)


def _write_csv(df: pd.DataFrame, path: str, mode: Literal["w", "a", "x"] = "w") -> None:
    """
    Writes a DataFrame to a csv file.
    """
    write_cols = [col for col in df.columns.tolist() if col != Column.TRANSACTION_ID]
    for col in write_cols:
        df[col] = df[col].astype(str)

    df.to_csv(
        path,
        index=False,
        mode=mode,
        columns=write_cols,
    )


def _write_numbers(
    df: pd.DataFrame, path: str, mode: Literal["w", "a", "x"] = "w"
) -> None:
    """
    Writes a DataFrame to a numbers file.
    """
    raise NotImplementedError("Writing to a .numbers file is not currently supported.")


def _write_excel(
    df: pd.DataFrame, path: str, mode: Literal["w", "a", "x"] = "w"
) -> None:
    """
    Writes a DataFrame to a xlsx file.
    """
    if mode == "x":
        raise NotImplementedError(
            "Writing to excel with mode 'x' is not currently supported."
        )

    with pd.ExcelWriter(
        path, engine="openpyxl", mode=mode, if_sheet_exists="overlay"
    ) as writer:
        sheet_name = next(iter(writer.sheets))
        df.to_excel(
            writer,
            sheet_name=sheet_name,
            index=False,
            startrow=0 if mode == "w" else writer.sheets[sheet_name].max_row,
            header=mode == "w",
        )
