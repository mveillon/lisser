import yaml
import pandas as pd
from functools import reduce
from operator import __and__, __or__

from typing import Callable, Any, Dict

from src.utilities.paths import config_path
from src.read_config.filter import Filter
from src.read_config.agg_function import AggFunction
from src.utilities.column import Column

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

    num_days = max((df[Column.DATE.value].max() - df[Column.DATE.value].min()).days, 1)

    res = {}
    for agg in data["aggregations"]:
        agg_data = data["aggregations"][agg]

        if len(agg_data["filters"]) > 0:
            conjunction = reduce(
                __or__ if agg_data.get("disjunction", False) else __and__,
                map(lambda f: Filter(**f).filter_cond(df), agg_data["filters"]),
            )

            filtered = df.loc[conjunction]

        else:
            filtered = df

        res[agg] = AggFunction(**agg_data["agg"]).aggregate(filtered, num_days)

    return res
