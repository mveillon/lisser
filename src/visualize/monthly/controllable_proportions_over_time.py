import pandas as pd
from os.path import join

from src.visualize.common import metrics_over_time
from src.calculations.controllable_proportions import controllable_proportions
from src.utilities.df_grouping import group_by_month


def controllable_proportions_over_time(df: pd.DataFrame, out_dir: str):
    """
    Plots the proportions of money spent that was controllable, not controllable,
    compared to how much was earned.

    Parameters:
        df (DataFrame): a Pandas DataFrame to plot
        out_dir (str): the directory to put the plots in

    Returns:
        None
    """
    weeks, partitions = group_by_month(df)
    control_ot = []
    not_control_ot = []
    saved_ot = []

    for p in partitions:
        control, not_control, earned = controllable_proportions(p)
        control_ot.append(control)
        not_control_ot.append(not_control)
        saved_ot.append(earned - (control + not_control))

    metrics_over_time(
        weeks,
        {
            "controllable": (control_ot, "b"),
            "not_controllable": (not_control_ot, "r"),
            "saved": (saved_ot, "g"),
        },
        "Controllable proportions over time",
        join(out_dir, "controllable_proportions_over_time.png"),
    )
