import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from os.path import join
from typing import Dict
from datetime import timedelta

from src.models.day_counts import DayCounts
from src.utilities.helpers import monthly_income
from src.read_data.column import Column


def saved_over_time(df: pd.DataFrame, out_dir: str) -> None:
    """
    Plots how much was saved over the course of the DataFrame
    with a line plot.

    Parameters:
        df (DataFrame): a Pandas DataFrame
        out_dir (str): the directory to put the plot in

    Returns:
        None
    """
    fmt = "%m/%d/%Y"

    spent_by_date: Dict[str, float] = {}
    current = df[Column.DATE].min()
    end_date = df[Column.DATE].max()
    per_day = monthly_income() / DayCounts.days_per_month()
    while current <= end_date:
        spent_by_date[current.strftime(fmt)] = per_day
        current += timedelta(days=1)

    spending = df.groupby(Column.DATE)[Column.PRICE].sum()
    for dtm, spent in spending.to_dict().items():
        spent_by_date[dtm.strftime(fmt)] -= spent

    all_dates = np.array(list(spent_by_date.keys()))
    inds = sorted(range(all_dates.shape[0]), key=all_dates.__getitem__)
    x = all_dates[inds]
    y = np.cumsum(np.array(list(spent_by_date.values()))[inds])

    days_of_year = np.arange(y.shape[0], dtype=int)
    poly_model = np.polynomial.Polynomial.fit(days_of_year, y, 3)
    trend = poly_model(days_of_year)

    plt.clf()
    plt.title("Total Saved over Time")
    plt.ylabel("Total Income Added")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(bymonthday=[1]))
    plt.plot(x, y, "b", label="Saved")
    plt.plot(x, np.cumsum(np.full(y.shape, per_day * 0.2)), "g", label="Goal")
    plt.plot(x, trend, "--b", label="trend")
    plt.legend()

    plt.savefig(join(out_dir, "total_saved.png"))
    plt.close()
