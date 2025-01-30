from typing import Callable, Dict, no_type_check
from dataclasses import dataclass

from src.utilities.dictionary_ops import convert_dict


def dataclass_from_json(converters: Dict[str, Callable] = {}) -> Callable[[type], type]:
    """
    Decorator that converts the class to a dataclass, but with the added functionality
    of being able to parse a JSON with attributes.

    Parameters:
        converters (Dict[str, Callable]): mapping of key values in the dictionary
            to functions to convert them

    Returns:
        new_type (type): the type with the added functionality
    """

    def inner(cls: type) -> type:
        dc: type = dataclass(cls)
        old_init: Callable = dc.__init__  # type: ignore

        @no_type_check
        def new_init(self, *args, **kwargs) -> None:
            if len(args) == 1 and isinstance(args[0], dict):
                convert_dict(args[0], converters)
                old_init(self, **args[0])

            else:
                old_init(self, *args, **kwargs)

        dc.__init__ = new_init  # type: ignore
        return dc

    return inner
