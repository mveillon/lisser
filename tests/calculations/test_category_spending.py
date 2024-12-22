import numpy as np

from src.calculations.category_spending import category_spending

from tests.test_utils import sample_data


def test_category_spending():
    data = sample_data()

    cats = category_spending(data)

    assert np.isclose(cats["Total spent"], 1520.89)
    assert np.isclose(cats["Groceries"], 89.28)

    for spent in cats.values():
        assert spent > 0
