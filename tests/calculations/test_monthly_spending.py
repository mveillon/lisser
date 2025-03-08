import numpy as np

from src.calculations.monthly_spending import monthly_spending

from tests.test_utils import sample_data


def test_monthly_spending():
    data = sample_data()

    months = monthly_spending(data)
    print(months)
    assert np.isclose(months["Jan"], 1620, atol=10)
    assert np.isclose(months["Feb"], 80, atol=5)
