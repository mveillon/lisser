import yaml
import pandas as pd
from functools import reduce
from operator import __and__

from typing import List, Callable, Any, Dict

from src.utilities.paths import config_path
from src.read_config.filter import Filter
from src.read_config.agg_function import AggFunction

type AggFunc = Callable[[pd.DataFrame], Any]


def custom_aggregations(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Performs all custom aggregations on df.

    Parameters:
        df (DataFrame): the Pandas DataFrame to aggregate

    Returns:
        aggs (Dict[str, Any]): a mapping of agg name to value
    """
    with open(config_path(), "r") as c:
        data = yaml.safe_load(c)

    res = {}
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

        res[agg] = AggFunction(**data["aggregations"][agg]["agg"]).aggregate(filtered)

    return res
