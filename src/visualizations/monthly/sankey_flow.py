import pandas as pd
from os.path import join
from sankeyflow import Sankey
import matplotlib.pyplot as plt

from typing import List, NamedTuple, cast
from itertools import chain

from src.calculations.aggregations.estimated_income_after_tax import (
    estimated_income_after_tax,
)
from src.models.paths import Paths
from src.read_data.column import Column
from src.utilities.dictionary_ops import (
    NestedDict,
    dictionary_sum,
    recursive_divide,
)
from src.models.types import Number
from src.read_config.get_config import config_globals


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

    options = {}
    if source == "Income":
        options["flow_color_mode"] = "source"

    this_layer = []
    for label, branch in d.items():
        subtotal = dictionary_sum(branch)
        if subtotal > 0:
            this_layer.append(Flow(source, label, subtotal, options))

    this_layer.extend(
        chain(*[_get_flows(label, branch) for label, branch in d.items()])
    )
    return this_layer


def _graph_flows(flow: NestedDict, out_path: str, label_format: str) -> None:
    """
    Creates a graph of the given spending flow and saves it to out_path.
    """
    plt.clf()
    plt.figure(figsize=(12, 8))
    plt.title(f"Spending Flow for {Paths.get_year()}")

    s = Sankey(
        flows=_get_flows("Income", flow),
        node_opts={"label_format": label_format, "label_opts": {"fontsize": 8}},
    )
    for node_list in s.nodes:
        for node in node_list:
            if len(node.outflows) > 0:
                node.label_pos = "left"
            else:
                node.label_pos = "right"

    s.draw()
    plt.savefig(out_path)
    plt.close()


def sankey_flow(df: pd.DataFrame, out_dir: str) -> None:
    """
    Plots where spending went in a Sankey chart.

    Parameters:
        df (DataFrame): a Pandas DataFrame
        out_dir (str): the directory to put the plot in

    Returns:
        None
    """
    total_spent = df[Column.PRICE].sum()
    total_income = estimated_income_after_tax(df)

    flow = {
        "Saved": total_income - total_spent,
        "Controllable": {"Other Controllable": 0},
        "Not Controllable": {"Food": {}, "Other Not Controllable": 0},
    }

    cats = df.groupby([Column.CATEGORY])[Column.CONTROLLABLE].mean()

    for cat, controllable_prop in cats.items():
        control_key = (
            "Controllable" if round(controllable_prop) == 1 else "Not Controllable"
        )

        this_cat = df.loc[df[Column.CATEGORY] == cat]
        cat_spent = this_cat[Column.PRICE].sum()
        cat_t = (
            cast(str, cat).title()
            if cat_spent > total_spent * config_globals()["SANKEY_OTHER_THRESHOLD"]
            else f"Other {control_key}"
        )

        flow[control_key][cat_t] = flow[control_key].get(cat_t, 0) + cat_spent

    desc_col = "Description"
    if desc_col in df.columns:
        bills_flow = {
            bill_name: sub_df[Column.PRICE].sum()
            for bill_name, sub_df in df.loc[df[Column.CATEGORY] == "Bills"].groupby(
                desc_col
            )
        }
        bills_total = sum(bills_flow.values())

        items = list(bills_flow.items())  # eagerly load indices before iteration
        for desc, total in items:
            if total <= bills_total * config_globals()["SANKEY_OTHER_THRESHOLD"]:
                del bills_flow[desc]
                bills_flow["Other bills"] = bills_flow.get("Other bills", 0) + total

        if len(bills_flow) > 1:
            flow["Not Controllable"]["Bills"] = bills_flow

    _graph_flows(
        flow,
        join(out_dir, "sankey.png"),
        "{label}\n${value:,.0f}",
    )
    _graph_flows(
        recursive_divide(flow, total_income / 100),
        join(out_dir, "sankey_percentage.png"),
        "{label}\n{value:.2f}%",
    )
