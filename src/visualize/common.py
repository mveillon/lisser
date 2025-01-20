import numpy as np
import pandas as pd
from typing import Union, Dict, Tuple
from os import mkdir
from os.path import exists, join
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from src.utilities.helpers import monthly_income, format_currency
from src.utilities.column import Column
from src.utilities.paths import sheet_dir
from src.utilities.read_data import read_data
from src.calculations.category_spending import category_spending


def compare_months(
    month_1: Union[str, pd.DataFrame],
    month_2: str,
    out_dir: str,
    income=monthly_income(),
):
    """
    Compares the two months by category. If `month_2 = ''`, it will just plot
    the by_category numbers for the single month.

    Parameters:
        month_1 (Union[str, pd.DataFrame]): the sheet to plot. If month_2 is populated,
            this should be a string so the legend is accurate.
        month_2 (str): the sheet to compare to month_1 by category. If this is empty,
            this function will just make a bar plot of month_1 by category
        out_dir (str): the directory to put the plot in
        income (int): the monthly income to compare the spending to. Defaults to
            `helpers.monthly_income()`.

    Returns:
        None
    """
    if not exists(out_dir):
        mkdir(out_dir)

    if isinstance(month_1, str):
        df_1 = read_data(join(sheet_dir(), month_1 + ".xlsx"))
        colors = [{"color": "b", "label": month_1}, {"color": "g", "label": month_2}]
    else:
        df_1 = month_1
        colors = [{}, {}]

    cats_1 = category_spending(df_1, income=income)

    num_weeks = (df_1[Column.DATE].max() - df_1[Column.DATE].min()).days // 7

    if month_2:
        df_2 = read_data(join(sheet_dir(), month_2 + ".xlsx"))
        cats_2 = category_spending(df_2, income=income)

        for cat in cats_1:
            if cat not in cats_2:
                cats_2[cat] = 0
        for cat in cats_2:
            if cat not in cats_1:
                cats_1[cat] = 0

        sorted_keys = sorted(
            cats_1.keys(), key=lambda cat: cats_1[cat] + cats_2[cat], reverse=True
        )

        items = [
            [sorted_keys, list(map(cats_1.__getitem__, sorted_keys))],
            [sorted_keys, list(map(cats_2.__getitem__, sorted_keys))],
        ]

    else:
        sorted_keys = sorted(cats_1.keys(), key=cats_1.__getitem__, reverse=True)
        items = [[sorted_keys, list(map(cats_1.__getitem__, sorted_keys))]]

    plt.clf()
    plt.figure().set_figwidth(10 + 5 * (len(items) - 1))
    plt.title(f"Spending by category over {num_weeks} weeks")
    plt.ylabel("Dollars")
    plt.gcf().subplots_adjust(bottom=0.2)

    for i, (keys, values) in enumerate(items):
        inds = np.arange(len(keys))
        width = 0.4 + 0.4 * (2 - len(items))

        bar = plt.bar(inds + width * i, values, width, **colors[i])
        plt.xticks(inds + width * (len(items) - 1) / 2, keys, rotation=50)
        plt.bar_label(bar, map(format_currency, values), rotation=70)

    if isinstance(month_1, str) or month_2 != "":
        plt.legend()
    plt.savefig(join(out_dir, "by_category.png"))


def metrics_over_time(
    weeks: np.ndarray, metrics: Dict[str, Tuple[np.ndarray, str]], title: str, out: str
):
    """
    Plots how much was spent in each metric.

    Parameters:
        df (DataFrame): the Pandas DataFrame to analyze. Should have a column
            at least for each string in `cols`
        weeks (np.ndarray): an array of dates, corresponding to the amounts spent in the
            arrays in `metrics`
        metrics (Dict[str, np.ndarray]): a mapping of metric name to a tuple of [how
            much was spent in the weeks in `weeks`, the line formatting]
        title (str): the title of the plot
        out (str): the path to save the plot to

    Returns:
        None
    """
    plt.clf()
    plt.title(title)
    plt.ylabel("Dollars Spent")
    plt.xlabel("Week start")

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%m/%d/%Y"))
    kwargs = {"interval": 7} if len(weeks) <= 5 else {"bymonthday": 1}
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(**kwargs))

    for metric_name, (values, style) in metrics.items():
        plt.plot(
            weeks,
            values,
            style,
            **({} if metric_name == "" else {"label": metric_name}),
        )

    plt.gcf().autofmt_xdate()
    if len(metrics) > 1:
        plt.legend()

    plt.savefig(out)
