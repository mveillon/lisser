import pandas as pd
from typing import Tuple

from src.calculations.expenses_split import expenses_split


def income_split(
    df: pd.DataFrame,
) -> Tuple[Tuple[str, str], Tuple[str, str], Tuple[str, str]]:
    """
    Returns the split of income, recording how much was
    controllable, not controllable, and how much was saved. Also
    records the goals for these.

    Parameters:
        df (DataFrame): a Pandas DataFrame

    Returns:
        split (Tuple[Tuple]]): a tuple of (label, percentage) tuples,
            one for each category
    """
    not_c, c, saved = expenses_split(df)
    return (
        ("Not Controllable Percentage", f"{not_c}%"),
        ("Controllable Percentage", f"{c}%"),
        ("Saved Percentage", f"{saved}%"),
    )
