import pandas as pd
from os.path import join

from sankeyflow import Sankey
import matplotlib.pyplot as plt

from src.aggregations.total_saved import total_saved
from src.aggregations.estimated_income_after_tax import estimated_income_after_tax

from src.utilities.read_data import read_data
from src.utilities.paths import untracked_path, get_year
from src.utilities.column import Column


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
    total_spent = df[Column.PRICE.value].sum()

    flow = {
        "Saved": total_saved(df),
        "Controllable": {"Other": 0},
        "Not Controllable": {"Food": {}, "Other": 0},
    }

    cats = df.groupby([Column.CATEGORY.value])[Column.CONTROLLABLE.value].mean()

    for cat, controllable_prop in cats.items():
        this_cat = df.loc[df[Column.CATEGORY.value] == cat]
        cat_spent = this_cat[Column.PRICE.value].sum()
        is_other = cat_spent < total_spent * 0.05

        cat_t = cat.title()
        if round(this_cat[Column.IS_FOOD.value].mean()) == 1:
            flow["Not Controllable"]["Food"][cat_t] = (
                flow["Not Controllable"]["Food"].get(cat_t, 0) + cat_spent
            )

        elif round(controllable_prop) == 1:
            if is_other:
                flow["Controllable"]["Other"] += cat_spent
            else:
                flow["Controllable"][cat_t] = (
                    flow["Controllable"].get(cat_t, 0) + cat_spent
                )

        else:
            if is_other:
                flow["Not Controllable"]["Other"] += cat_spent
            else:
                flow["Not Controllable"][cat_t] = (
                    flow["Not Controllable"].get(cat_t, 0) + cat_spent
                )

    sub_dict_sum = lambda d: (
        sum(map(sub_dict_sum, d.values())) if isinstance(d, dict) else d
    )

    dict_to_node_list = lambda d: [
        (cat, sub_dict_sum(branch)) for cat, branch in d.items()
    ]

    not_other = lambda d: {k: v for k, v in d.items() if k != "Other"}

    nodes = [
        [("Income", estimated_income_after_tax(df))],
        [
            ("Saved", sub_dict_sum(flow["Saved"])),
            ("Controllable", sub_dict_sum(flow["Controllable"])),
            ("Not Controllable", sub_dict_sum(flow["Not Controllable"])),
        ],
        dict_to_node_list(not_other(flow["Controllable"]))
        + [
            (
                "Other",
                flow["Controllable"]["Other"] + flow["Not Controllable"]["Other"],
            )
        ]
        + dict_to_node_list(not_other(flow["Not Controllable"])),
        dict_to_node_list(flow["Not Controllable"]["Food"]),
    ]

    flows = [
        ("Income", "Saved", nodes[1][0][1], {"flow_color_mode": "source"}),
        ("Income", "Controllable", nodes[1][1][1], {"flow_color_mode": "source"}),
        ("Income", "Not Controllable", nodes[1][2][1], {"flow_color_mode": "source"}),
        *[
            ("Controllable", cat, sub_dict_sum(d))
            for cat, d in not_other(flow["Controllable"]).items()
        ],
        ("Controllable", "Other", flow["Controllable"]["Other"]),
        ("Not Controllable", "Other", flow["Not Controllable"]["Other"]),
        *[
            ("Not Controllable", cat, sub_dict_sum(d))
            for cat, d in not_other(flow["Not Controllable"]).items()
        ],
        *[
            ("Food", cat, sub_dict_sum(d))
            for cat, d in flow["Not Controllable"]["Food"].items()
        ],
    ]

    plt.clf()
    plt.figure(figsize=(15, 8))
    plt.title(f"Spending Flow for {get_year()}")

    s = Sankey(
        flows=flows,
        nodes=nodes,
    )
    s.draw()
    plt.savefig(join(out_dir, "sankey.png"))
