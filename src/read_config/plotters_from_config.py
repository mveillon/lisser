import numpy as np
import pandas as pd
from typing import Tuple, List, cast
from operator import __or__, __and__
from functools import reduce
from os.path import join

from src.models.config_objs.plot import Plot
from src.read_config.get_config import get_config
from src.models.types import Plotter
from src.utilities.df_common import (
    group_by_month,
    group_by_week,
    filter_large_transactions,
)
from src.read_data.column import Column

from src.visualizations.common import metrics_over_time


def _read_convert_plots() -> List[Plot]:
    """
    Reads the config.yml and converts all dataclasses.

    Parameters:
        None

    Returns:
        plots (List[Plot]): a list of converted plots
    """
    data = get_config()["plots"]

    for plot in data:
        new_lines = []
        for line in data[plot]["lines"]:
            if "agg" in line:
                for agg in line["agg"]:
                    new_lines.append(line | {"agg": agg})

            else:
                new_lines.append(line)

        data[plot]["lines"] = new_lines
        data[plot]["plot_name"] = plot

    return list(map(Plot, data.values()))  # type: ignore


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
        plotter = cast(Plotter, lambda df, out: create_plot(plot, df, out))
        if plot.timeframe == "monthly":
            monthlys.append(plotter)
        elif plot.timeframe == "yearly":
            yearlys.append(plotter)
        else:
            raise ValueError(f"Invalid timeframe: {plot.timeframe}")

    return monthlys, yearlys


def create_plot(plot: Plot, df: pd.DataFrame, out_dir: str) -> None:
    """
    Writes the plot to the correct path.

    Parameters:
        plot (Plot): a Plot object specifying how to create the plot
        df (DataFrame): a Pandas DataFrame to plot
        out_dir (str): the directory to put the plots in

    Returns:
        None
    """
    filt_total = 0.0
    if plot.timeframe == "monthly":
        starts, partitions = group_by_week(df)
    elif plot.timeframe == "yearly":
        starts, partitions = group_by_month(df)
    else:
        raise ValueError(f"Invalid timeframe: {plot.timeframe}")

    metrics = {}
    for line in plot.lines:
        if len(line.filters) == 0:
            y_vals = list(map(lambda p: p[Column.PRICE].sum(), partitions))

        else:
            y_vals = []
            for part in partitions:
                conjunction = reduce(
                    __or__ if line.disjunction else __and__,
                    map(lambda f: f.filter_cond(part), line.filters),
                )

                part_filt, to_add = filter_large_transactions(part.loc[conjunction])
                y_vals.append(part_filt[Column.PRICE].sum())
                filt_total += to_add

        y_vals_arr = np.array(y_vals) + (filt_total / len(y_vals))
        if line.agg is not None:
            y_vals_arr = np.full(
                len(partitions), getattr(np, line.agg.func)(y_vals_arr)
            )

        metrics[line.label] = (y_vals_arr, line.style)

    metrics_over_time(
        np.array(starts),
        metrics,
        plot.title,
        join(out_dir, plot.plot_name + ".png"),
    )
