import pandas as pd
from typing import Dict

from src.calculations.expenses_split import expenses_split
from src.utilities.read_data import read_data
from src.utilities.paths import untracked_path


def income_split(df: pd.DataFrame) -> Dict[str, Dict[str, str]]:
    """
    Returns the split of income, recording how much was
    controllable, not controllable, and how much was saved. Also
    records the goals for these.

    Parameters:
        df (DataFrame): a Pandas DataFrame

    Returns:
        split (Dict[str, Dict[str, str]]): a dictionary of information
            about the income split
    """
    not_c, c, saved = expenses_split(pd.concat([df, read_data(untracked_path())]))
    return {
        "Not Controllable": {"actual": f"{not_c}%", "goal": "<=50%"},
        "Controllable": {"actual": f"{c}%", "goal": "<=30%"},
        "Saved": {"actual": f"{saved}%", "goal": ">=20%"},
    }
