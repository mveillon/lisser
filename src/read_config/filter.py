from dataclasses import dataclass
from typing import Literal, Any, Callable
import pandas as pd
from operator import __eq__, __gt__, __lt__, __ge__, __le__

OperatorFunction = Callable[[pd.Series, Any], pd.Series]


@dataclass
class Filter:
    """
    A way to a filter a DataFrame by comparing a column to a literal value.

    Attributes:
        column (str): which column of the DataFrame to compare
        operator (str): how to compare the column to the value
        value (Any): the value to compare to those of the column
    """

    column: str
    operator: Literal["=", ">", "<", "<=", ">=", "contains", "icontains", "in"]
    value: Any

    def _convert_operator(self) -> OperatorFunction:
        """
        Parses `self.operator` and returns a function that can be called.

        Parameters:
            None

        Returns:
            filterer (OperatorFunction): the function that can be called to filter df
        """
        mapping = {
            "=": __eq__,
            ">": __gt__,
            "<": __lt__,
            "<=": __le__,
            ">=": __ge__,
            "contains": lambda series, val: series.str.contains(
                val, case=True, regex=False
            ),
            "icontains": lambda series, val: series.str.contains(
                val, case=False, regex=False
            ),
            "iequals": lambda series, val: series.str.casefold() == val.casefold(),
            "in": lambda series, val: series.isin(val),
        }
        return mapping[self.operator]

    def filter_cond(self, df: pd.DataFrame) -> pd.Series:
        """
        Returns a filter that can be applied to the DataFrame based on the attributes.

        Parameters:
            df (DataFrame): the Pandas DataFrame to filter

        Returns:
            col (DataFrame): a series of booleans that can filter df
        """
        return self._convert_operator()(df[self.column], self.value)
