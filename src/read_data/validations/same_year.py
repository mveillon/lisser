import pandas as pd

from src.read_data.column import Column


def same_year(df: pd.DataFrame) -> None:
    """
    Checks that every row in df has the same year.

    Parameters:
        df (DataFrame): the DataFrame to validate

    Returns:
        None
    """
    if len(set(df[Column.DATE].dt.year)) > 1:
        raise ValueError(
            "Validation error: every year in the Date column must be the same."
        )
