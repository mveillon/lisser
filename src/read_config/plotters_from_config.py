from typing import Tuple, List, cast

from src.read_config.plot import Plot
from src.read_config.get_config import get_config
from src.utilities.types import Plotter


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
        if plot.timeframe == "monthly":
            monthlys.append(cast(Plotter, plot.create_plot))
        elif plot.timeframe == "yearly":
            yearlys.append(cast(Plotter, plot.create_plot))
        else:
            raise ValueError(f"Invalid timeframe: {plot.timeframe}")

    return monthlys, yearlys
