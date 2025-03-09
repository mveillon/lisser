import pandas as pd
import pytest
from datetime import datetime

from src.read_data.validations.same_year import same_year
from src.read_data.column import Column


def test_same_year():
    df = pd.DataFrame(
        {
            Column.DATE: [
                datetime(2025, 3, 7),
                datetime(2025, 3, 8),
                datetime(2024, 3, 9),
            ]
        }
    )

    with pytest.raises(ValueError):
        same_year(df)

    df = pd.DataFrame({Column.DATE: [datetime(2025, 3, 7), datetime(2025, 3, 8)]})

    same_year(df)
