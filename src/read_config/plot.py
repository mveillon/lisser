from typing import Literal, List
import numpy as np
import pandas as pd
from os.path import join

from itertools import starmap
from functools import reduce
from operator import __and__, __or__

from src.read_config.line import Line
from src.utilities.df_grouping import group_by_month, group_by_week
from src.utilities.column import Column
from src.visualize.common import metrics_over_time
from src.utilities.decorators import dataclass_from_json


@dataclass_from_json(converters={"lines": lambda lst: list(starmap(Line, lst))})
class Plot:
    """
    One plot to generate.

    Attributes:
        plot_name (str): the name of the file that will contain this graph
        title (str): the title at the top of the graph
        timeframe (str): over what timeframe to aggregate the data. Either "yearly"
            or "monthly"
        lines (List[Line]): a list of lines to include in the plot
    """

    plot_name: str
    title: str
    timeframe: Literal["yearly", "monthly"]
    lines: List[Line]

    def create_plot(self, df: pd.DataFrame, out_dir: str) -> None:
        """
        Writes the plot to the correct path.

        Parameters:
            df (DataFrame): a Pandas DataFrame to plot
            out_dir (str): the directory to put the plots in

        Returns:
            None
        """
        if self.timeframe == "monthly":
            starts, partitions = group_by_week(df)
        elif self.timeframe == "yearly":
            starts, partitions = group_by_month(df)
        else:
            raise ValueError(f"Invalid timeframe: {self.timeframe}")

        metrics = {}
        for line in self.lines:
            if len(line.filters) == 0:
                y_vals = list(map(lambda p: p[Column.PRICE].sum(), partitions))

            else:
                y_vals = []
                for part in partitions:
                    conjunction = reduce(
                        __or__ if line.disjunction else __and__,
                        map(lambda f: f.filter_cond(part), line.filters),
                    )
                    y_vals.append(part.loc[conjunction][Column.PRICE].sum())

            if line.agg is None:
                y_vals_arr = np.array(y_vals)
            else:
                y_vals_arr = np.full(
                    len(partitions), getattr(np, line.agg.func)(y_vals)
                ).tolist()

            metrics[line.label] = (y_vals_arr, line.style)

        metrics_over_time(
            np.array(starts),
            metrics,
            self.title,
            join(out_dir, self.plot_name + ".png"),
        )
