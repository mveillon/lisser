from os import listdir, getcwd
from os.path import basename, sep, splitext, join, abspath
from pathlib import Path
import pandas as pd
from importlib import import_module
from inspect import getmembers, isfunction, getfile
import yaml
from typing import List, Callable, Union, Any

from src.utilities.paths import aggregation_path, sheet_dir
from src.utilities.helpers import format_currency
from src.utilities.read_data import combined_df
from src.read_config.custom_aggregations import custom_aggregations


class AggregationDriver:
    """
    Class to perform all aggregations.
    """

    def __init__(self):
        pass

    def _get_agg_files(self) -> List[str]:
        """
        Returns all the files with aggregation functions.

        Paramters:
            None

        Returns:
            files (List[str]): the list of paths
        """
        exclude = {"__init__.py"}
        agg_folder = (Path(__file__).parent / "aggregations").resolve()
        return [
            join(str(agg_folder), mod)
            for mod in listdir(agg_folder)
            if basename(mod) not in exclude and splitext(mod)[1] == ".py"
        ]

    def _get_module(self, file: str) -> str:
        """
        Converts the path of a Python file to a module. Assumes
        the file is inside of the cwd.

        Parameters:
            file (str): the path of the python file

        Returns:
            module (str): the module name
        """
        raw = splitext(abspath(file)[len(abspath(getcwd())) :])[0].replace(sep, ".")
        return raw[int(raw.startswith(".")) : len(raw) - int(raw.endswith("."))]

    def _get_agg_funcs(
        self, path: str
    ) -> List[Union[Callable[[pd.DataFrame], int], Callable[[pd.DataFrame], float]]]:
        """
        Finds all the functions in the module at `path`.

        Parameters:
            path (str): the module to inspect

        Returns:
            funcs (List[Callable]): a list of functions that take a DataFrame and
                return a number
        """
        return [
            func
            for (name, func) in getmembers(
                import_module(self._get_module(path)), isfunction
            )
            if not name.startswith("_") and getfile(func) == path
        ]

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

        for path in self._get_agg_files():
            for func in self._get_agg_funcs(path):
                out[to_title(func.__name__)] = format_out(func(spending))

        for title, agg_val in custom_aggregations(spending).items():
            out[to_title(title)] = format_out(agg_val)

        with open(aggregation_path(), "w") as f:
            yaml.dump(out, f, default_flow_style=False, sort_keys=False)
