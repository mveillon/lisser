import pandas as pd
from typing import Dict

from src.utilities.helpers import monthly_income
from src.read_data.column import Column
from src.models.day_counts import DayCounts


def category_spending(df: pd.DataFrame) -> Dict[str, float]:
    """
    Calculates how much was spent on each category, as well as how much was
    spent in total and how much was made in that period.

    Parameters:
        df (DataFrame): the Pandas DataFrame to analyze

    Returns:
        categories (Dict[str, float]): mapping from category name to how much
            was spent on that category
    """
    totals = df.groupby([Column.CATEGORY])[Column.PRICE].sum()

    # we add one so the range is inclusive of both ends
    num_days = (df[Column.DATE].max() - df[Column.DATE].min()).days + 1
    prorated_income = num_days * monthly_income() / DayCounts.days_per_month()

    x = list(totals.index) + ["Total spent", "Income"]
    y = list(totals.values) + [df[Column.PRICE].sum(), prorated_income]
    return dict(zip(x, y))
