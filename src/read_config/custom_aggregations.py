import pandas as pd
from functools import reduce
from operator import __and__, __or__

from typing import Any, Dict

from src.models.config_objs.filter import Filter
from src.models.config_objs.agg_function import AggFunction
from src.read_config.get_config import get_config


def custom_aggregations(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Performs all custom aggregations on df.

    Parameters:
        df (DataFrame): the Pandas DataFrame to aggregate

    Returns:
        aggs (Dict[str, Any]): a mapping of agg name to value
    """
    data = get_config()["aggregations"]

    res = {}
    for agg in data:
        agg_data = data[agg]

        if len(agg_data["filters"]) > 0:
            conjunction = reduce(
                __or__ if agg_data.get("disjunction", False) else __and__,
                map(lambda f: Filter(**f).filter_cond(df), agg_data["filters"]),
            )

            filtered = df.loc[conjunction]

        else:
            filtered = df

        res[agg] = AggFunction(**agg_data["agg"]).aggregate(filtered)

    return res
