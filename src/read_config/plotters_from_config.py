from typing import Tuple, List


from src.models.config_objs.plot import Plot
from src.read_config.get_config import get_config
from src.models.types import Plotter


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
        data[plot]["plot_name"] = plot

    return [Plot(p) for p in data.values()]  # type: ignore


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
    plots: List[Plot] = _read_convert_plots()

    monthlys: List[Plotter] = []
    yearlys: List[Plotter] = []
    for plot in plots:
        if plot.timeframe not in ("monthly", "yearly"):
            raise ValueError(f"Invalid timeframe: {plot.timeframe}")

        plot_list = monthlys if plot.timeframe == "monthly" else yearlys
        plot_list.append(plot.create_plot)

    return monthlys, yearlys
