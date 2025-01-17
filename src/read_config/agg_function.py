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
        divide (bool): whether to divide the outcome into weekly, monthly, and yearly
            chunks. Default is False.
        column (str): which column to aggregate. Default is None, which should only
            be used if `func` is "count"
    """

    func: str
    divide: bool = False
    column: str = None

    def aggregate(self, df: pd.DataFrame, num_days: int) -> Any:
        """
        Aggregates the DataFrame based on the attributes.

        Parameters:
            df (DataFrame): the filtered Pandas DataFrame to aggregate
            num_days (int): over how many days the total span of data was

        Returns:
            agg_value (Any): the value of the aggregation
        """
        if self.func == "count":
            return df.shape[0]

        if self.column is None:
            raise ValueError("Column must be provided.")

        res = df[self.column].__getattr__(self.func)().item()

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
