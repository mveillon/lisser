from dataclasses import dataclass
from typing import Any
import pandas as pd


@dataclass
class AggFunction:
    """
    A function to aggregate a column of a Pandas DataFrame.

    Attributes:
        func (str): which function to use for aggregation. Should be a method
            of pd.Series and should take no arguments
        column (str): which column to aggregate. Default is None, which should only
            be used if `func` is "count"
    """

    func: str
    column: str = None

    def aggregate(self, df: pd.DataFrame) -> Any:
        """
        Aggregates the DataFrame based on the attributes.

        Parameters:
            df (DataFrame): the Pandas DataFrame to aggregate

        Returns:
            agg_value (Any): the value of the aggregation
        """
        if self.func == "count":
            return df.shape[0]

        if self.column is None:
            raise ValueError("Column must be provided.")

        return df[self.column].__getattr__(self.func)()
