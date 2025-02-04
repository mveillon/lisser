import numpy as np
import pandas as pd
from os.path import join
import matplotlib.pyplot as plt

from src.utilities.helpers import format_currency
from src.calculations.category_spending import category_spending


def spent_by_category(df: pd.DataFrame, out_dir: str) -> None:
    """
    Plots spending by category, compared to prorated monthly income,
    the default of which is set to helpers.monthly_income() with a bar plot.

    Parameters:
        df (DataFrame): a Pandas DataFrame to plot.
        out_dir (str): the directory to put the plot in

    Returns:
        None
    """
    cats = category_spending(df)
    sorted_keys = sorted(cats.keys(), key=cats.__getitem__, reverse=True)
    sorted_vals = list(map(cats.__getitem__, sorted_keys))

    plt.clf()
    plt.figure().set_figwidth(10)
    plt.figure().set_figheight(7)
    plt.title("Spending by category")
    plt.ylabel("Total spent")
    plt.gcf().subplots_adjust(bottom=0.2)

    inds = np.arange(len(sorted_keys))
    bar = plt.bar(inds, sorted_vals, 0.8)
    plt.xticks(inds, sorted_keys, rotation=50)
    plt.bar_label(bar, list(map(format_currency, sorted_vals)), rotation=70)

    plt.savefig(join(out_dir, "by_category.png"))
    plt.close()
