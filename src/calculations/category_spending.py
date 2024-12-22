import pandas as pd
from typing import Dict

from src.utilities.helpers import monthly_income
from src.utilities.column import Column


def category_spending(
    df: pd.DataFrame, income: int = monthly_income()
) -> Dict[str, float]:
    """
    Calculates how much was spent on each category, as well as how much was
    spent in total and how much was made in that period.

    Parameters:
        df (DataFrame): the Pandas DataFrame to analyze
        income (int): the monthly income to compare to. Defaults to
            `helpers.monthly_income()`

    Returns:
        categories (Dict[str, float]): mapping from category name to how much
            was spent on that category
    """
    totals = df.groupby([Column.CATEGORY.value])[Column.PRICE.value].sum()

    # we add one so the range is inclusive of both ends
    num_days = (df[Column.DATE.value].max() - df[Column.DATE.value].min()).days + 1
    prorated_income = num_days * income * 12 / 365

    x = list(totals.index) + ["Total spent", "Income"]
    y = list(totals.values) + [df[Column.PRICE.value].sum(), prorated_income]
    return dict(zip(x, y))
