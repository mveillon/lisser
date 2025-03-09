import pandas as pd

from src.calculations.aggregations.estimated_income_after_tax import (
    estimated_income_after_tax,
)
from src.calculations.aggregations.total_spent import total_spent


def total_saved(df: pd.DataFrame) -> float:
    """
    Returns the total amount saved.

    Parameters:
        df (DataFrame): a Pandas DataFrame

    Returns:
        saved (float): how much was saved
    """
    return estimated_income_after_tax(df) - total_spent(df)
