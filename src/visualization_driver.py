import pandas as pd
from os import listdir, mkdir
from os.path import join, exists, basename
from shutil import rmtree
from typing import List

from src.utilities.paths import (
    sheet_dir,
    plots_dir,
    staging_dir,
    month_from_path,
    get_out_dir,
    is_excel,
    untracked_path,
)
from src.utilities.read_data import read_data, combined_df
from src.utilities.helpers import find_big_bills

from src.visualize.weekly.controllable_bars import controllable_bars
from src.visualize.weekly.spent_by_category import spent_by_category
from src.visualize.weekly.spent_by_week import spent_by_week

from src.visualize.monthly.spent_by_month import spent_by_month
from src.visualize.monthly.saved_over_time import saved_over_time
from src.visualize.monthly.controllable_proportions_over_time import (
    controllable_proportions_over_time,
)

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

    def __init__(self):
        for dir in (staging_dir(), plots_dir(), join(plots_dir(), "Combined")):
            if not exists(dir):
                mkdir(dir)

        find_big_bills()

        self.monthlys, self.yearlys = plotters_from_config()

    def _plot_df(self, df: pd.DataFrame, out_dir: str):
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
        controllable_bars(df, out_dir)
        spent_by_category(df, out_dir)
        spent_by_week(df, out_dir)

        for m in self.monthlys:
            m(df, out_dir)

    def visualize(self):
        """
        Creates plots of all the spreadsheets. Main driver for
        the visualizations.

        Parameters:
            None

        Returns:
            None
        """
        for path in listdir(sheet_dir()):
            if is_excel(path) and basename(path) != basename(untracked_path()):
                df = read_data(join(sheet_dir(), path))
                self._plot_df(df, get_out_dir(month_from_path(path)))

        all_dfs = combined_df(sheet_dir())
        combined_path = join(plots_dir(), "Combined")

        spent_by_month(all_dfs)
        plot_funcs = [
            self._plot_df,
            saved_over_time,
            controllable_proportions_over_time,
            *self.yearlys,
        ]
        for f in plot_funcs:
            f(all_dfs, combined_path)

        rmtree(staging_dir())
