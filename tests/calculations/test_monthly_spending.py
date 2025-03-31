import numpy as np

from src.calculations.monthly_spending import monthly_spending

from tests.test_utils import sample_data


def test_monthly_spending():
    data = sample_data()

    months = monthly_spending(data)
    assert np.isclose(months["Jan"], 731.39, rtol=0.1)
    assert np.isclose(months["Feb"], 120.35, rtol=0.1)
