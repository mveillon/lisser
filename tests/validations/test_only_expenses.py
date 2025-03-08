import pandas as pd
import pytest

from src.validations.only_expenses import only_expenses
from src.utilities.column import Column


def test_only_expenses():
    df = pd.DataFrame(
        {
            Column.PRICE: [1.50, 2.50, -3.00],
        }
    )

    with pytest.raises(ValueError):
        only_expenses(df)

    df = pd.DataFrame({Column.PRICE: [1.50, 2.50]})

    only_expenses(df)
