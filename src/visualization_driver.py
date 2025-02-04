import pandas as pd
from os import mkdir
from os.path import join, exists
from shutil import rmtree
from typing import List
from pathlib import Path

from src.utilities.paths import Paths
from src.utilities.read_data import read_data, get_month_dfs
from src.utilities.get_funcs_from_module import (
    get_funcs_from_module,
    get_modules_from_folder,
)
from src.utilities.column import Column

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
        for dir in (
            Paths.staging_dir(),
            Paths.plots_dir(),
            join(Paths.plots_dir(), "Combined"),
        ):
            if not exists(dir):
                mkdir(dir)

        self.monthlys, self.yearlys = plotters_from_config()

        visualizers = Path(__file__).parent / "visualize"

        for mod in get_modules_from_folder(str(visualizers / "monthly")):
            for func in get_funcs_from_module(mod):
                self.monthlys.append(func)

        for mod in get_modules_from_folder(str(visualizers / "yearly")):
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
        if out_dir[-1] != "/":
            out_dir += "/"
        if not exists(out_dir):
            mkdir(out_dir)

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
            self._plot_df(
                df,
                join(
                    Paths.plots_dir(),
                    month,
                ),
            )

        combined_path = join(Paths.plots_dir(), "Combined")

        plot_funcs = [
            self._plot_df,
            *self.yearlys,
        ]
        for f in plot_funcs:
            f(all_dfs, combined_path)

        rmtree(Paths.staging_dir())
