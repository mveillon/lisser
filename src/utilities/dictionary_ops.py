from typing import Union, Dict, List, Tuple, Any
from numbers import Number

NestedDict = Union[Number, Dict[str, "NestedDict"]]
Node = Tuple[str, Number]
Flow = Tuple[str, str, Number, Dict[str, Any]]


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


def _dict_to_node_list(d: NestedDict) -> List[Node]:
    """
    Converts the top layer of the tree into one layer of nodes.
    """
    return [(cat, dictionary_sum(branch)) for cat, branch in d.items()]


def _not_other(d: Dict[str, NestedDict]) -> NestedDict:
    """
    Returns a filtered copy of the dictionary not including the "Other"
    key. Assumes d has at least one layer.
    """
    return {k: v for k, v in d.items() if k != "Other"}


def _filter_zeros(lst: List[Tuple], cost_ind: int) -> List[Tuple]:
    """
    Filters out the tuples with a zero at cost_ind.
    """
    return [t for t in lst if t[cost_ind] > 0]


def nodes_from_dict(flow_dict: NestedDict) -> List[List[Node]]:
    """
    Returns the nodes, in the format expected from the sankeyflow module,
    from a nested dictionary representing the tree. Does not include the
    source layer.

    Parameters:
        flow (NestedDict): a tree of money spent

    Returns:
        nodes (List[List[Node]]): the flow in the format
            expected from sankeyflow
    """

    return list(
        map(
            lambda lst: _filter_zeros(lst, 1),
            [
                [
                    ("Saved", dictionary_sum(flow_dict["Saved"])),
                    ("Controllable", dictionary_sum(flow_dict["Controllable"])),
                    ("Not Controllable", dictionary_sum(flow_dict["Not Controllable"])),
                ],
                _dict_to_node_list(_not_other(flow_dict["Controllable"]))
                + [
                    (
                        "Other",
                        flow_dict["Controllable"]["Other"]
                        + flow_dict["Not Controllable"]["Other"],
                    )
                ]
                + _dict_to_node_list(_not_other(flow_dict["Not Controllable"])),
                _dict_to_node_list(flow_dict["Not Controllable"]["Food"]),
            ],
        )
    )


def flow_array_from_dict(flow_dict: NestedDict) -> List[Flow]:
    """
    Converts the flow dictionary into a list of flows as expected from the
    sankeyflow module. Does not include source flows.

    Parameters:
        flow_dict (NestedDict): the tree of spending

    Returns:
        flow_arr (List[NestedDict]): the flow as an array of tuples
    """
    return _filter_zeros(
        [
            *[
                ("Controllable", cat, dictionary_sum(d))
                for cat, d in _not_other(flow_dict["Controllable"]).items()
            ],
            *[
                (control_key, "Other", flow_dict[control_key]["Other"])
                for control_key in ["Controllable", "Not Controllable"]
            ],
            *[
                ("Not Controllable", cat, dictionary_sum(d))
                for cat, d in _not_other(flow_dict["Not Controllable"]).items()
            ],
            *[
                ("Food", cat, dictionary_sum(d))
                for cat, d in flow_dict["Not Controllable"]["Food"].items()
            ],
        ],
        2,
    )


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
        if new_val == {}:
            continue
        if isinstance(new_val, dict) and k in d1:
            if not isinstance(d1[k], dict):
                raise ValueError(
                    "YAML merge error. "
                    + f"Key `{k}` is dictionary in overwrite but not base."
                )

            recursive_merge(d1[k], new_val)

        else:
            d1[k] = new_val
