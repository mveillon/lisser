import pandas as pd
from typing import cast

from src.read_data.column import Column


def total_spent(df: pd.DataFrame) -> float:
    """
    Returns how much money was spent in total.

    Parameters:
        df (DataFrame): a Pandas DataFrame

    Returns:
        spent (float): the total amount spent
    """
    return cast(float, df[Column.PRICE].sum())
