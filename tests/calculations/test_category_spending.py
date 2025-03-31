import numpy as np

from src.calculations.category_spending import category_spending

from tests.test_utils import sample_data


def test_category_spending():
    data = sample_data()

    cats = category_spending(data)

    assert np.isclose(cats["Total spent"], 4200.81)
    assert np.isclose(cats["Groceries"], 1065.88)

    for cat, spent in cats.items():
        if cat != "Income":
            assert spent > 0.0
