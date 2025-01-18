from src.utilities.dictionary_ops import (
    dictionary_sum,
)


def test_dictionary_sum():
    d = {
        "l6": {"l7": 6},
        "l0": 10,
        "l1": {"l2": 3, "l4": {"l5": 19}},
        "l8": "hello world",
    }

    assert dictionary_sum(5) == 5
    assert dictionary_sum(d) == 38
