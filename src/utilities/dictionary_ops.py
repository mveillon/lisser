from typing import Union, Dict, List, Tuple, Any
from numbers import Number

NestedDict = Union[Number, Dict[str, "NestedDict"]]
Node = Tuple[str, Number]
Flow = Tuple[str, str, Number, Dict[str, Any]]


def dictionary_sum(d: NestedDict) -> Number:
    """
    Recursively sums the numeric leaves of the dictionary. The
    leaves are not required to al be numeric.

    Params:
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


def nodes_from_dict(flow_dict: NestedDict) -> List[List[Node]]:
    """
    Returns the nodes, in the format expected from the sankeyflow module,
    from a nested dictionary representing the tree. Does not include the
    source layer.

    Params:
        flow (NestedDict): a tree of money spent

    Returns:
        nodes (List[List[Node]]): the flow in the format
            expected from sankeyflow
    """
    return [
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
    ]


def flow_array_from_dict(flow_dict: NestedDict) -> List[Flow]:
    """
    Converts the flow dictionary into a list of flows as expected from the
    sankeyflow module. Does not include source flows.

    Params:
        flow_dict (NestedDict): the tree of spending

    Returns:
        flow_arr (List[NestedDict]): the flow as an array of tuples
    """
    return [
        *[
            ("Controllable", cat, dictionary_sum(d))
            for cat, d in _not_other(flow_dict["Controllable"]).items()
        ],
        ("Controllable", "Other", flow_dict["Controllable"]["Other"]),
        ("Not Controllable", "Other", flow_dict["Not Controllable"]["Other"]),
        *[
            ("Not Controllable", cat, dictionary_sum(d))
            for cat, d in _not_other(flow_dict["Not Controllable"]).items()
        ],
        *[
            ("Food", cat, dictionary_sum(d))
            for cat, d in flow_dict["Not Controllable"]["Food"].items()
        ],
    ]
