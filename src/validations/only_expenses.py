import pandas as pd

from src.utilities.column import Column


def only_expenses(df: pd.DataFrame) -> None:
    """
    Checks that every row is an expense and that the price is above zero.

    Parameters:
        df (DataFrame): the DataFrame to validate

    Returns:
        None
    """
    if df.loc[df[Column.PRICE] <= 0].shape[0]:
        raise ValueError(
            "Validation error: every value in Price column must be above zero."
        )
