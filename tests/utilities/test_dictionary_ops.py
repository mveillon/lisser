from src.utilities.dictionary_ops import (
    dictionary_sum,
    recursive_merge,
    recursive_index,
    convert_dict,
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


def test_recursive_merge():
    base = {
        "a": 1,
        "b": 2,
        "c": {
            "d": 1,
            "e": 2,
            "f": {"g": 3},
        },
        "d": 0,
        "i": {"j": 4},
    }

    expected = {
        "a": 1,
        "b": 2,
        "c": {
            "d": 1,
            "e": 2,
            "f": {"g": 3},
        },
        "d": 0,
        "i": {"j": 4},
    }

    recursive_merge(base, {})
    assert base == expected

    overwrite = {
        "a": -1,
        "c": {
            "f": {
                "g": -3,
            }
        },
        "h": -10,
        "i": {},
    }

    expected = {
        "a": -1,
        "b": 2,
        "c": {
            "d": 1,
            "e": 2,
            "f": {
                "g": -3,
            },
        },
        "d": 0,
        "i": {"j": 4},
        "h": -10,
    }

    recursive_merge(base, overwrite)
    assert base == expected


def test_recursive_index():
    base = {
        "a": 1,
        "b": 2,
        "c": {
            "d": 1,
            "e": 2,
            "f": {"g": 3},
        },
        "d": 0,
        "i": {"j": 4},
    }

    assert recursive_index(base, []) == base
    assert recursive_index(base, ["a"]) == 1
    assert recursive_index(base, ["c", "d"]) == 1
    assert recursive_index(base, ["c", "f"]) == {"g": 3}


def test_convert_dict():
    base = {
        "a": "hello world",
        "b": {
            "c": 40,
        },
        "d": {
            "e": 80,
        },
    }
    converters = {"b": lambda d: d["c"], "e": lambda n: n * 2}

    expected = {
        "a": "hello world",
        "b": 40,
        "d": {
            "e": 160,
        },
    }

    convert_dict(base, converters)
    assert base == expected
