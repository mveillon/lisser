from dataclasses import dataclass
from typing import Any
import pandas as pd
import math

from src.utilities.column import Column


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
    divide: bool = False
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

        res = df[self.column].__getattr__(self.func)().item()

        num_days = (df[Column.DATE.value].max() - df[Column.DATE.value].min()).days
        if self.divide:
            divisors = {
                "total": 1,
                "yearly": num_days / 365,
                "monthly": num_days / (365 / 12),
                "weekly": num_days / 7,
            }

            return {k: res / v for k, v in divisors.items()}

        else:
            return res
