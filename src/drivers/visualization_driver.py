import pandas as pd
from os import makedirs
from os.path import join
from typing import List

from src.read_data.paths import Paths
from src.read_data.read_data import read_data, get_month_dfs
from src.utilities.get_funcs_from_module import (
    get_funcs_from_module,
    get_modules_from_folder,
)
from src.read_data.column import Column

from src.read_config.plotters_from_config import plotters_from_config, Plotter


class VisualizationDriver:
    """
    Class to perform all visualizations.

    Attributes:
        monthlys (List[Plotter]): the plotters to call each month
        yearlys (List[Plotters]): the plotters to call each year
    """

    monthlys: List[Plotter]
    yearlys: List[Plotter]

    def __init__(self) -> None:
        makedirs(join(Paths.plots_dir(), "Combined"), exist_ok=True)
        self.monthlys, self.yearlys = plotters_from_config()

        visualizers = join("src", "visualizations")

        for mod in get_modules_from_folder(join(visualizers, "monthly")):
            for func in get_funcs_from_module(mod):
                self.monthlys.append(func)

        for mod in get_modules_from_folder(join(visualizers, "yearly")):
            for func in get_funcs_from_module(mod):
                self.yearlys.append(func)

    def _plot_df(self, df: pd.DataFrame, out_dir: str) -> None:
        """
        Makes a bunch of plots for the dataframe and puts them in the `out_dir`
        directory.

        Parameters:
            df (DataFrame): a Pandas DataFrame to plot
            out_dir (str): the out_dir path to put the plots in

        Returns:
            None
        """
        for m in self.monthlys:
            m(df, out_dir)

    def visualize(self) -> None:
        """
        Creates plots of all the spreadsheets. Main driver for
        the visualizations.

        Parameters:
            None

        Returns:
            None
        """
        all_dfs = read_data(Paths.spending_path())
        months = get_month_dfs(all_dfs)
        for df in months:
            dates_in_df = list(df.sort_values(Column.DATE)[Column.DATE])
            month = dates_in_df[len(dates_in_df) // 2].strftime("%B")
            out_dir = join(Paths.plots_dir(), month)
            makedirs(out_dir, exist_ok=True)
            self._plot_df(df, out_dir)

        combined_path = join(Paths.plots_dir(), "Combined")
        plot_funcs = [
            self._plot_df,
            *self.yearlys,
        ]
        for f in plot_funcs:
            f(all_dfs, combined_path)
