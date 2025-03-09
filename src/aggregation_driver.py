import pandas as pd
from pathlib import Path
from typing import Any, Dict, List

from src.utilities.day_counts import DayCounts
from src.utilities.paths import Paths
from src.utilities.helpers import format_currency
from src.utilities.read_data import read_data
from src.read_config.custom_aggregations import custom_aggregations
from src.utilities.get_funcs_from_module import (
    get_funcs_from_module,
    get_modules_from_folder,
)
from src.utilities.column import Column


class AggregationDriver:
    """
    Class to perform all aggregations.
    """

    num_days: int

    def _get_aggs(self) -> Dict[str, Any]:
        """
        Performs all the aggregations and formats them into a dictionary.
        """
        spending = read_data(Paths.spending_path())
        self.num_days = (spending[Column.DATE].max() - spending[Column.DATE].min()).days
        out = {}

        to_title = lambda s: s.replace("_", " ").title()

        for path in get_modules_from_folder(
            str(Path(__file__).parent / "aggregations")
        ):
            for func in get_funcs_from_module(path):
                agg_val = func(spending)
                if hasattr(agg_val, "__iter__") and not isinstance(agg_val, str):
                    for label, amount in agg_val:
                        out[to_title(label)] = amount

                else:
                    out[to_title(func.__name__)] = agg_val

        for title, agg_val in custom_aggregations(spending).items():
            out[to_title(title)] = agg_val

        return out

    def _format_cell(self, val: Any, as_money: bool) -> str:
        """
        Formats the cell value into something that can go in a spreadsheet.
        """
        if isinstance(val, float):
            if as_money:
                return format_currency(val)

            return str(round(val, 2))

        return str(val)

    def aggregate(self) -> None:
        """
        Performs a series of aggregations writes the output to the
        plots directory.

        Parameters:
            None

        Returns:
            None
        """
        aggs = self._get_aggs()

        cols: Dict[str, List[str]] = {
            "Description": [],
            "Total Amount": [],
            "Yearly": [],
            "Monthly": [],
            "Weekly": [],
        }

        for label, amount in aggs.items():
            to_add = {
                "Description": label,
            }
            if isinstance(amount, int) or isinstance(amount, float):
                per_day = amount / self.num_days
                is_money = isinstance(amount, float)
                to_add |= {
                    "Total Amount": self._format_cell(amount, is_money),
                    "Yearly": self._format_cell(
                        per_day * DayCounts.days_per_year(), is_money
                    ),
                    "Monthly": self._format_cell(
                        per_day * DayCounts.days_per_month(), is_money
                    ),
                    "Weekly": self._format_cell(
                        per_day * DayCounts.days_per_week(), is_money
                    ),
                }

            else:
                to_add |= {
                    "Total Amount": str(amount),
                    "Yearly": "",
                    "Monthly": "",
                    "Weekly": "",
                }

            for col, val in to_add.items():
                cols[col].append(val)

        pd.DataFrame(cols).to_csv(
            Paths.aggregation_path(),
            index=False,
        )
