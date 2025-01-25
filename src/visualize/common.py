import numpy as np
from typing import Dict, Tuple
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def metrics_over_time(
    weeks: np.ndarray, metrics: Dict[str, Tuple[np.ndarray, str]], title: str, out: str
) -> None:
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
        args = (weeks, values, style)
        if metric_name == "":
            plt.plot(*args)
        else:
            plt.plot(*args, label=metric_name)

    plt.gcf().autofmt_xdate()
    if len(metrics) > 1:
        plt.legend()

    plt.savefig(out)
    plt.close()
