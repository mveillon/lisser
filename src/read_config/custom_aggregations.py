import yaml
import pandas as pd
from functools import reduce
from operator import __and__

from typing import List, Callable, Any, Tuple

from src.utilities.paths import config_path
from src.read_config.filter import Filter
from src.read_config.agg_function import AggFunction

type AggFunc = Callable[[pd.DataFrame], Any]


def custom_aggregations(df: pd.DataFrame) -> Tuple[List[str], List[Any]]:
    """
    Performs all custom aggregations on df.

    Parameters:
        df (DataFrame): the Pandas DataFrame to aggregate

    Returns:
        titles (List[str]): the list of snake_case titles of aggregations
        agg_values (List[Any]): the list of aggregated value
    """
    with open(config_path(), "r") as c:
        data = yaml.safe_load(c)

    titles = list(data["aggregations"].keys())
    res = []

    for agg in data["aggregations"]:
        filts = data["aggregations"][agg]["filters"]

        if len(filts) > 0:
            conjunction = reduce(
                __and__,
                map(lambda f: Filter(**f).filter_cond(df), filts),
            )

            filtered = df.loc[conjunction]

        else:
            filtered = df

        res.append(AggFunction(**data["aggregations"][agg]["agg"]).aggregate(filtered))

    return titles, res
