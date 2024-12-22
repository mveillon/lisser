import numpy as np

from src.calculations.monthly_spending import monthly_spending

from tests.test_utils import sample_data


def test_monthly_spending():
    data = sample_data()

    months = monthly_spending(data)
    print(months)
    assert np.isclose(months["Jan"], 1510.02)
    assert np.isclose(months["Feb"], 1217.38)
