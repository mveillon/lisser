import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from os.path import join

from src.calculations.monthly_spending import monthly_spending
from src.utilities.helpers import monthly_income, format_currency
from src.utilities.column import Column


def spent_by_month(df: pd.DataFrame, out_dir: str) -> None:
    """
    Plots how much was spent each month using a line plot.

    Parameters:
        df (DataFrame): a Pandas DataFrame to plot
        out_dir (str): the directory to put the plot in

    Returns:
        None
    """
    months = monthly_spending(df)
    total_days = (df[Column.DATE].max() - df[Column.DATE].min()).days
    average = (
        ((df[Column.PRICE].sum() / total_days) * (365 / 12)) if total_days > 0 else 0
    )

    plt.clf()
    fig = plt.figure()
    ax = fig.add_subplot()

    plt.title("Spending By Month")
    plt.ylabel("Total Spent")

    x = sorted(months, key=lambda d: datetime.strptime(f"1 {d} 2024", "%d %b %Y"))
    y = list(map(months.__getitem__, x))
    inds = np.arange(len(x))
    plt.xticks(inds, x)

    plt.plot(inds, y, label="Total spent")
    plt.plot(inds, np.full(inds.shape[0], average), "g", label="Average")
    plt.plot(inds, np.full(inds.shape[0], monthly_income()), "r", label="Income")
    plt.plot(inds, np.full(inds.shape[0], monthly_income() * 0.8), "y", label="Goal")
    plt.legend(loc="upper right")

    for x_loc, y_loc in zip(inds, y):
        ax.annotate(format_currency(y_loc), (x_loc, y_loc))

    plt.savefig(join(out_dir, "spent_per_month.png"))
    plt.close()
