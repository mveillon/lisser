from os.path import join, basename

from src.utilities.get_funcs_from_module import (
    get_funcs_from_module,
    get_modules_from_folder,
)


def _sample_modules():
    return join("tests", "sample_modules")


def test_get_modules_from_folder():
    expected = ["sample_mod1.py", "sample_mod2.py"]
    result = sorted(list(map(basename, get_modules_from_folder(_sample_modules()))))

    assert result == expected


def test_get_funcs_from_module():
    expected1 = ["func1", "func2"]
    result1 = sorted(
        list(
            map(
                lambda f: f.__name__,
                get_funcs_from_module(join(_sample_modules(), "sample_mod1.py")),
            )
        )
    )

    assert expected1 == result1

    expected1 = ["func3", "func4", "func5"]
    result1 = sorted(
        list(
            map(
                lambda f: f.__name__,
                get_funcs_from_module(join(_sample_modules(), "sample_mod2.py")),
            )
        )
    )

    assert expected1 == result1
