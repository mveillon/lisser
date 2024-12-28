from pathlib import Path
import yaml
from typing import Any

from src.utilities.paths import aggregation_path, sheet_dir
from src.utilities.helpers import format_currency
from src.utilities.read_data import combined_df
from src.read_config.custom_aggregations import custom_aggregations
from src.utilities.get_funcs_from_module import (
    get_funcs_from_module,
    get_modules_from_folder,
)


class AggregationDriver:
    """
    Class to perform all aggregations.
    """

    def __init__(self):
        pass

    def aggregate(self):
        """
        Performs a series of aggregations writes the output to the
        plots directory.

        Parameters:
            None

        Returns:
            None
        """
        spending = combined_df(sheet_dir())
        out = {}

        to_title = lambda s: s.replace("_", " ").title()

        def format_out(val: Any) -> Any:
            if isinstance(val, dict):
                return {k: format_out(v) for k, v in val.items()}

            if isinstance(val, float):
                return format_currency(val)

            return val

        for path in get_modules_from_folder(
            (Path(__file__).parent / "aggregations").resolve()
        ):
            for func in get_funcs_from_module(path):
                out[to_title(func.__name__)] = format_out(func(spending))

        for title, agg_val in custom_aggregations(spending).items():
            out[to_title(title)] = format_out(agg_val)

        with open(aggregation_path(), "w") as f:
            yaml.dump(out, f, default_flow_style=False, sort_keys=False)
