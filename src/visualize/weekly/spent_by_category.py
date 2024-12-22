import pandas as pd

from src.utilities.helpers import monthly_income
from src.visualize.common import compare_months


def spent_by_category(df: pd.DataFrame, out_dir: str, income: int = monthly_income()):
    """
    Plots spending by category, compared to prorated monthly income,
    the default of which is set to helpers.monthly_income() with a bar plot.

    Parameters:
        df (DataFrame): a Pandas DataFrame to plot.
        out_dir (str): the directory to put the plot in
        income (int): the monthly income to compare spending to. Defaults
            to `helpers.monthly_income()`

    Returns:
        None
    """
    compare_months(df, "", out_dir, income=income)
