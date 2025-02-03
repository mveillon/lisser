from pathlib import Path
import yaml
from typing import Any

from src.utilities.paths import Paths
from src.utilities.helpers import format_currency
from src.utilities.read_data import read_data
from src.read_config.custom_aggregations import custom_aggregations
from src.utilities.get_funcs_from_module import (
    get_funcs_from_module,
    get_modules_from_folder,
)


class AggregationDriver:
    """
    Class to perform all aggregations.
    """

    def aggregate(self) -> None:
        """
        Performs a series of aggregations writes the output to the
        plots directory.

        Parameters:
            None

        Returns:
            None
        """
        spending = read_data(Paths.spending_path())
        out = {}

        to_title = lambda s: s.replace("_", " ").title()

        def format_out(val: Any) -> Any:
            if isinstance(val, dict):
                return {k: format_out(v) for k, v in val.items()}

            if isinstance(val, float):
                return format_currency(val)

            return val

        for path in get_modules_from_folder(
            str(Path(__file__).parent / "aggregations")
        ):
            for func in get_funcs_from_module(path):
                out[to_title(func.__name__)] = format_out(func(spending))

        for title, agg_val in custom_aggregations(spending).items():
            out[to_title(title)] = format_out(agg_val)

        with open(Paths.aggregation_path(), "w") as f:
            yaml.dump(out, f, default_flow_style=False, sort_keys=False)
