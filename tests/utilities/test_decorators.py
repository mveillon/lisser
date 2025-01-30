from dataclasses import dataclass, asdict
from src.utilities.decorators import dataclass_from_json


class DataclassFromJsonTestClass:
    var_name: str
    var_val: int
    src: dict
    var_is_negative: bool = False


def test_dataclass_from_json():
    convert_str = lambda s: s.replace("_", " ").capitalize()
    deco1 = dataclass
    deco2 = dataclass_from_json(converters={"var_name": convert_str})

    fields = {
        "var_name": "secret_to_the_universe",
        "var_val": 42,
    }
    fields["src"] = {k: v for k, v in fields.items()}

    var1 = deco1(DataclassFromJsonTestClass)(**fields)
    var1.var_name = convert_str(var1.var_name)
    var1.src["var_name"] = convert_str(var1.src["var_name"])

    var2 = deco2(DataclassFromJsonTestClass)(fields)

    assert sorted(asdict(var1).items()) == sorted(asdict(var2).items())
