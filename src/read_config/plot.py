from typing import Literal, List
import numpy as np
import pandas as pd
from os.path import join

from functools import reduce
from operator import __and__, __or__

from src.read_config.line import Line
from src.utilities.df_common import (
    group_by_month,
    group_by_week,
    filter_large_transactions,
)
from src.utilities.column import Column
from src.visualize.common import metrics_over_time
from src.utilities.decorators import dataclass_from_converted_json


@dataclass_from_converted_json(
    converters={"lines": lambda lst: list(map(Line, lst))}  # type: ignore
)
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
        filt_total = 0
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

                    part_filt, to_add = filter_large_transactions(part.loc[conjunction])
                    y_vals.append(part_filt[Column.PRICE].sum())
                    filt_total += to_add

            y_vals_arr = np.array(y_vals) + (filt_total / len(y_vals))
            if line.agg is not None:
                y_vals_arr = np.full(
                    len(partitions), getattr(np, line.agg.func)(y_vals_arr)
                ).tolist()

            metrics[line.label] = (y_vals_arr, line.style)

        metrics_over_time(
            np.array(starts),
            metrics,
            self.title,
            join(out_dir, self.plot_name + ".png"),
        )
