import numpy as np

from src.calculations.controllable_proportions import controllable_proportions

from tests.test_utils import sample_data


def test_controllable_proportions():
    data = sample_data()

    controllable, not_control, income = controllable_proportions(data)

    assert np.isclose(controllable, 255.36)
    assert np.isclose(not_control, 1265.53)
    assert np.isclose(income, 9707.65, atol=200)
