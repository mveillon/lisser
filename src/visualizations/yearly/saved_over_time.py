import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from os.path import join
from typing import cast, List

from src.models.day_counts import DayCounts
from src.utilities.helpers import monthly_income, get_weeks
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
    fmt = "%b"
    payments = get_weeks(df[Column.DATE].min(), df[Column.DATE].max())
    dates = []
    balance_changes = []
    expected_saved = [0.0]
    for dtm in payments:
        dates.append(dtm)
        made = monthly_income() / DayCounts.weeks_per_month()
        balance_changes.append(made)
        expected_saved.append(expected_saved[-1] + (made * 0.2))

    expected_saved = expected_saved[1:]

    spending = df.groupby(Column.DATE)[Column.PRICE].sum()
    for date, spent in spending.to_dict().items():
        dates.append(date)
        balance_changes.append(-spent)

    inds = sorted(range(len(dates)), key=dates.__getitem__)
    x = np.array(dates)[inds]
    sorted_changes = np.array(balance_changes)[inds]
    balance = [0.0]
    for change in sorted_changes:
        balance.append(balance[-1] + change)

    y = np.array(balance)[1:]

    days_of_year = np.fromiter(
        map(lambda d: int(d.strftime("%j")), x),
        dtype=int,
        count=x.shape[0],
    )
    poly_model = np.polynomial.Polynomial.fit(days_of_year, y, 3)
    trend = poly_model(days_of_year)

    plt.clf()
    plt.title("Total Saved over Time")
    plt.ylabel("Total Income Added")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(fmt))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(bymonthday=[1]))
    plt.plot(x, y, "b", label="Saved")
    plt.plot(cast(List[int], payments), expected_saved, "g", label="Goal")
    plt.plot(x, trend, "--b", label="trend")
    plt.legend()

    plt.savefig(join(out_dir, "total_saved.png"))
    plt.close()
