import pandas as pd
import pytest

from src.read_data.validations.empty_dataframe import empty_dataframe


def test_empty_dataframe():
    df = pd.DataFrame({"col1": [], "col2": []})

    with pytest.raises(ValueError):
        empty_dataframe(df)

    df = pd.DataFrame({"col1": [1], "col2": [2]})

    empty_dataframe(df)
