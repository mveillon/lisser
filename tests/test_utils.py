import pandas as pd
from functools import lru_cache

from src.read_data.read_data import read_data


@lru_cache(maxsize=1)
def sample_data() -> pd.DataFrame:
    """
    Returns the sample data for use in tests.

    Parameters:
        None

    Returns:
        sample (DataFrame): a small DataFrame for testing
    """
    return read_data("sample_data.xlsx")
