import numpy as np
import pandas as pd
from os.path import join

from src.utilities.helpers import monthly_income, get_weeks
from src.utilities.column import Column
from src.calculations.weekly_projection import weekly_projection
from src.visualize.common import metrics_over_time


def spent_by_week(df: pd.DataFrame, out_dir: str, income: int = monthly_income()):
    """
    Plots spending by week smoothed out as a per month average, compared to the monthly
    income, which by default is helpers.monthly_income() with a line plot.

    Parameters:
        df (DataFrame): a Pandas DataFrame to plot
        out_dir (str): the directory to put the plots in
        income (int): the monthly income to compare spending to. Defaults to
            `helpers.monthly_income()`

    Returns:
        None
    """
    weeks = get_weeks(df[Column.DATE].min(), df[Column.DATE].max())
    avgs = weekly_projection(df)
    income_arr = np.full(len(avgs), income)
    avg_arr = np.full(len(avgs), np.average(avgs))

    metrics_over_time(
        weeks,
        {
            "actual": (avgs, "b"),
            "": (avgs, "bo"),
            "goal": (income_arr, "g"),
            "average": (avg_arr, "r"),
        },
        "Prorated spending per week",
        join(out_dir, "by_week.png"),
    )
