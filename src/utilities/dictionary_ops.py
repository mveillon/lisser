from typing import Union, Dict, List, Any
from numbers import Number

NestedDict = Union[Number, Dict[str, "NestedDict"]]


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
        return sum(
            map(
                dictionary_sum,
                [
                    sub_dict
                    for sub_dict in d.values()
                    if isinstance(sub_dict, dict) or isinstance(sub_dict, Number)
                ],
            )
        )

    return d


def recursive_merge(d1: Dict[str, Any], d2: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively merges `d2` into `d1`, keeping all keys from `d1`, but adding
    and preferring all key/value pairs in `d2`. `d1` is merged in place.

    Parameters:
        d1 (Dict[str, Any]): a potentially nested dictionary. Will be updated by this
            operation
        d2 (Dict[str, Any]): a potentially nested citionary whose values will be
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

            recursive_merge(d1[k], new_val)

        else:
            d1[k] = new_val


def recursive_index(d: Dict[str, Any], path: List[str]) -> Any:
    """
    Returns the branch of the nested dictionary, following the path
    of labels.

    Parameters:
        d (Dict[str, Any]): the tree to search

    Returns:
        branch (Any): the branch at the end of the path
    """
    current = d
    for label in path:
        current = current[label]

    return current
