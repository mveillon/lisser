import numpy as np

from src.calculations.expenses_split import expenses_split

from tests.test_utils import sample_data


def test_expenses_split():
    data = sample_data()

    not_control, control, saved = expenses_split(data, monthly_income=7750)

    assert np.isclose(not_control, 13.321, atol=1)
    assert np.isclose(control, 2.688, atol=1)
    assert np.isclose(saved, 83.991, atol=1)
