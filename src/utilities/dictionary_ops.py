from typing import Dict, Tuple, no_type_check, Callable, cast
import re

from src.models.types import Number, NestedDict


def dictionary_sum(d: NestedDict) -> Number:
    """
    Recursively sums the numeric leaves of the dictionary. The
    leaves are not required to al be numeric.

    Parameters:
        d (nested_dict): the tree of numbers

    Returns:
        total (Number): the total of all the leaves
    """
    if isinstance(d, dict):
        return sum(map(dictionary_sum, d.values()))

    try:
        _ = float(d)
        return d
    except ValueError:
        return 0


def recursive_merge(d1: Dict[str, NestedDict], d2: Dict[str, NestedDict]) -> None:
    """
    Recursively merges `d2` into `d1`, keeping all keys from `d1`, but adding
    and preferring all key/value pairs in `d2`. `d1` is merged in place.

    Parameters:
        d1 (Dict[str, NestedDict]): a potentially nested dictionary. Will be updated by
            this operation
        d2 (Dict[str, NestedDict]): a potentially nested citionary whose values will be
            preferred

    Returns:
        None
    """
    for k, new_val in d2.items():
        if isinstance(new_val, dict) and k in d1:
            if not isinstance(d1[k], dict):
                raise ValueError(
                    "YAML merge error. "
                    + f"Key `{k}` is dictionary in overwrite but not base."
                )

            recursive_merge(cast(Dict[str, NestedDict], d1[k]), new_val)

        else:
            d1[k] = new_val


@no_type_check
def recursive_index(
    d: Dict[str, NestedDict], path: Tuple[str, ...], set_to: Number | None = None
) -> Number:
    """
    Returns the branch of the nested dictionary, following the path
    of labels.

    Parameters:
        d (Dict[str, Any]): the tree to search
        path (Tuple[str, ...]): a tuple of sub-keys to index recursively
        set_to (Number): what to set as the new value. Defaults to None, at which point
            the value is not overwritten. If set, set_to will be returned

    Returns:
        branch (NestedDict): the branch at the end of the path, or set_to if it is set
    """
    current = d
    new_path = []
    lst_re = r"[^\[]*\[[0-9]+\]"
    to_int = lambda ind: int(re.sub(r"[^0-9]", "", ind))

    for label in path:
        if re.match(lst_re, label):
            parts = label.split("[")
            new_path.append(parts[0])
            new_path.extend([to_int(parts[i]) for i in range(1, len(parts))])
        else:
            new_path.append(label)

    if set_to is not None:
        last_ind = new_path.pop()

    for label in new_path:
        current = current[label]

    if set_to is not None:
        current[last_ind] = set_to
        return set_to

    return current


def convert_dict(d: dict, converters: Dict[str, Callable]) -> None:
    """
    Recursively converts all the values in d, modifying d in place.

    Parameters:
        d (dict): the potentially nested dictionary to convert
        converters (Dict[str, Callable]): a mapping of key names to
            functions to call on each value

    Returns:
        None
    """
    for k in d.keys() & converters.keys():
        d[k] = converters[k](d[k])

    for sub_d in filter(lambda b: isinstance(d[b], dict), d.keys()):
        convert_dict(d[sub_d], converters)


def recursive_divide(d: NestedDict, divisor: Number) -> NestedDict:
    """
    Recursively divides every value in d that supports division by the given divisor,
    returning a new dictionary.

    Parameters:
        d (NestedDict): the tree of numbers
        divisor (Number): what to divide the values by

    Returns:
        divided (NestedDict): the same tree of numbers, but with everything divided by
            divisor
    """
    if isinstance(d, dict):
        return {k: recursive_divide(branch, divisor) for k, branch in d.items()}

    try:
        return d / divisor
    except TypeError:
        return d
