import matplotlib.pyplot as plt
import pandas as pd
from os.path import join

from src.calculations.controllable_proportions import controllable_proportions
from src.utilities.helpers import format_currency
from src.utilities.df_common import filter_large_transactions


def controllable_bars(df: pd.DataFrame, out_dir: str) -> None:
    """
    Plots how much spending is controllable with a bar plot.

    Parameters:
        df (DataFrame): a Pandas DataFrame
        out_dir (str): the path to put the plot in

    Returns:
        None
    """
    plt.clf()

    plt.title("How much spending is controllable")
    plt.ylabel("Total spending")
    props = controllable_proportions(df)
    bar = plt.bar(["Controllable", "Not Controllable", "Total Income"], props)

    plt.bar_label(bar, list(map(format_currency, props)))

    plt.savefig(join(out_dir, "controllable.png"))
    plt.close()
