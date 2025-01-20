import pandas as pd

from typing import Callable, Tuple, List

from src.read_config.plot import Plot
from src.read_config.filter import Filter
from src.read_config.line import Line
from src.read_config.get_config import get_config

Plotter = Callable[[pd.DataFrame, str], None]


def _read_convert_plots() -> List[Plot]:
    """
    Reads the config.yml and converts all dataclasses.

    Parameters:
        None

    Returns:
        plots (List[Plot]): a list of converted plots
    """
    data = get_config()["plots"]

    res = []
    for plot in data:
        new_lines = []

        for line in data[plot]["lines"]:
            new_filts = []

            for filter in line["filters"]:
                new_filts.append(Filter(**filter))

            new_lines.append(Line(**(line | {"filters": new_filts})))

        res.append(Plot(**(data[plot] | {"lines": new_lines, "plot_name": plot})))

    return res


def plotters_from_config() -> Tuple[List[Plotter], List[Plotter]]:
    """
    Generates two lists of functions that will plot various metrics.

    Parameters:
        None

    Returns:
        monthlys (List[Plotter]): a list of functions to be called each month
        yearlys (List[Plotter]): a list of functions that should be called once
            per year
    """
    plots = _read_convert_plots()

    monthlys = []
    yearlys = []
    for plot in plots:
        if plot.timeframe == "monthly":
            monthlys.append(plot.create_plot)
        elif plot.timeframe == "yearly":
            yearlys.append(plot.create_plot)
        else:
            raise ValueError(f"Invalid timeframe: {plot.timeframe}")

    return monthlys, yearlys
