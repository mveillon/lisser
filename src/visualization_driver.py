import pandas as pd
from os import listdir, mkdir
from os.path import join, exists, basename
from shutil import rmtree
from typing import List
from pathlib import Path

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
from src.utilities.get_funcs_from_module import (
    get_funcs_from_module,
    get_modules_from_folder,
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

        visualizers = Path(__file__).parent / "visualize"

        for mod in get_modules_from_folder(str(visualizers / "monthly")):
            for func in get_funcs_from_module(mod):
                self.monthlys.append(func)

        for mod in get_modules_from_folder(str(visualizers / "yearly")):
            for func in get_funcs_from_module(mod):
                self.yearlys.append(func)

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

        plot_funcs = [
            self._plot_df,
            *self.yearlys,
        ]
        for f in plot_funcs:
            f(all_dfs, combined_path)

        rmtree(staging_dir())
