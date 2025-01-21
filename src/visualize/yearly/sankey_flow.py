import pandas as pd
from os.path import join
from sankeyflow import Sankey
import matplotlib.pyplot as plt

from typing import List, NamedTuple
from numbers import Number
from itertools import chain

from src.aggregations.estimated_income_after_tax import estimated_income_after_tax
from src.utilities.read_data import read_data
from src.utilities.paths import untracked_path, get_year
from src.utilities.column import Column
from src.utilities.dictionary_ops import (
    NestedDict,
    dictionary_sum,
)
from src.read_config.config_globals import config_globals


class Flow(NamedTuple):
    """
    A flow connecting two nodes.

    Attributes:
        source (str): the source of the flow
        dest (str): the destination of the flow
        flow_size (Number): how much money is flowing
        options (dict): optional dictionary passed to Sankey
    """

    source: str
    dest: str
    flow_size: Number
    options: dict = {}


def _get_flows(source: str, d: NestedDict) -> List[Flow]:
    """
    Returns all the flows in this subdictionary.
    """
    if not isinstance(d, dict):
        return []

    if source == "Income":
        options = {"flow_color_mode": "source"}
    else:
        options = {}

    this_layer = [
        Flow(
            source=source, dest=label, flow_size=dictionary_sum(branch), options=options
        )
        for label, branch in d.items()
    ]

    this_layer.extend(
        chain(*[_get_flows(label, branch) for label, branch in d.items()])
    )
    return this_layer


def sankey_flow(df: pd.DataFrame, out_dir: str):
    """
    Plots where spending went in a Sankey chart.

    Parameters:
        df (DataFrame): a Pandas DataFrame
        out_dir (str): the directory to put the plot in

    Returns:
        None
    """
    df = pd.concat([df, read_data(untracked_path())])
    total_spent = df[Column.PRICE].sum()

    flow: NestedDict = {
        "Saved": estimated_income_after_tax(df) - total_spent,
        "Controllable": {"Other": 0},
        "Not Controllable": {"Food": {}, "Other": 0},
    }

    cats = df.groupby([Column.CATEGORY])[Column.CONTROLLABLE].mean()

    for cat, controllable_prop in cats.items():
        this_cat = df.loc[df[Column.CATEGORY] == cat]
        cat_spent = this_cat[Column.PRICE].sum()
        cat_t = (
            cat.title()
            if cat_spent > total_spent * config_globals()["SANKEY_OTHER_THRESHOLD"]
            else "Other"
        )
        control_key = (
            "Controllable" if round(controllable_prop) == 1 else "Not Controllable"
        )

        if round(this_cat[Column.IS_FOOD].mean()) == 1:
            flow["Not Controllable"]["Food"][cat_t] = (
                flow["Not Controllable"]["Food"].get(cat_t, 0) + cat_spent
            )

        else:
            flow[control_key][cat_t] = flow[control_key].get(cat_t, 0) + cat_spent

    plt.clf()
    plt.figure(figsize=(15, 8))
    plt.title(f"Spending Flow for {get_year()}")

    s = Sankey(
        flows=_get_flows("Income", flow),
    )
    s.draw()
    plt.savefig(join(out_dir, "sankey.png"))
