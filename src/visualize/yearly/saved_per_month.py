import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from os.path import join
from datetime import datetime

from src.utilities.paths import Paths
from src.calculations.monthly_spending import monthly_spending
from src.utilities.helpers import monthly_income, format_currency


def saved_per_month(df: pd.DataFrame, out_dir: str) -> None:
    """
    Plots how much was saved over the course of the DataFrame,
    grouped by month.

    Parameters:
        df (DataFrame): a Pandas DataFrame
        out_dir (str): the directory to put the plot in

    Returns:
        None
    """
    months = monthly_spending(df)
    saved = {m: monthly_income() - spent for m, spent in months.items()}
    average = np.mean(list(saved.values()))

    plt.clf()
    fig = plt.figure()
    ax = fig.add_subplot()

    plt.title("Saved By Month")
    plt.ylabel("Saved that month")

    x = sorted(
        saved, key=lambda d: datetime.strptime(f"1 {d} {Paths.get_year()}", "%d %b %Y")
    )
    y = list(map(saved.__getitem__, x))
    inds = np.arange(len(x))
    plt.xticks(inds, x)

    plt.plot(inds, y, label="Total saved")
    plt.plot(inds, np.full(inds.shape[0], average), "g", label="Average")
    plt.plot(inds, np.full(inds.shape[0], monthly_income()), "r", label="Income")
    plt.plot(inds, np.full(inds.shape[0], monthly_income() * 0.2), "y", label="Goal")
    plt.legend(loc="upper right")

    for x_loc, y_loc in zip(inds, y):
        ax.annotate(format_currency(y_loc), (x_loc, y_loc))

    plt.savefig(join(out_dir, "saved_per_month.png"))
    plt.close()
