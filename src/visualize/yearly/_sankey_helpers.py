from typing import NamedTuple, Dict, List, Tuple
from numbers import Number

from src.utilities.dictionary_ops import NestedDict, recursive_index, dictionary_sum


class Node(NamedTuple):
    """
    A node in a node list, representing one category.

    Attributes:
        label (str): the label of the node
        subtotal (Number): how much was spent on this category
    """

    label: str
    subtotal: Number


class Flow(NamedTuple):
    """
    A flow connecting two nodes.

    Attributes:
        source (str): the source of the flow
        target (str): the destination of the flow
        flow_size (Number): how much money is flowing
    """

    source: str
    target: str
    flow_size: Number


class FlowTree(NamedTuple):
    """
    One node in the flow tree.

    Attributes:
        paths (List[List[str]]): all possible paths to this node, including the name of
            the node
        branches (Dict[str, FlowTree]): a dictionary mapping labels to subtrees
        leaves (Dict[str, List[FlowTree]]): a dictionary mapping leaf name to a list of
            nodes with the same name. Sharing a name is only allowed for leaves
    """

    paths: List[List[str]]
    branches: Dict[str, "FlowTree"]
    leaves: Dict[str, List["FlowTree"]]

    @staticmethod
    def _dict_convert_helper(flow_dict: NestedDict, path: List[str]) -> "FlowTree":
        """
        Helper function for the `from_flow_dict` function.
        """
        sub_flow = recursive_index(flow_dict, path)
        if not isinstance(sub_flow, dict):
            return FlowTree(
                paths=[path],
                branches=[],
                leaves=[],
            )

        branches = {}
        leaves = {}
        for label in sub_flow:
            new_path = path + [label]
            branches[label] = FlowTree._dict_convert_helper(flow_dict, new_path)

            # if len(branches[label].branches) == 0:
            #     if label in leaves:
            #         leaves[label][0].paths.append(new_path)
            #         leaves[label].append(branches[label])
            #         for leaf in leaves[label]:
            #             leaf.paths = leaves[label][0].paths

            #     else:
            #         leaves[label] = [branches[label]]

        return FlowTree(
            paths=[path],
            branches=branches,
            leaves=leaves,
        )

    @staticmethod
    def from_flow_dict(flow_dict: NestedDict) -> "FlowTree":
        """
        Returns a FlowTree from the nested dictionary.

        Parameters:
            flow_dict (NestedDict): the dictionary to convert to a tree. Should
                have at least one layer

        Returns:
            tree (FlowTree): the tree with the same information
        """
        return FlowTree._dict_convert_helper(flow_dict, [])

    def _raw_node_list(self, flow_dict: NestedDict) -> List[List[Node]]:
        """
        Converts the tree to a node list with no re-ordering.
        """
        res = []
        for label, branch in self.branches.items():
            subtotal = 0
            for leaf_paths in branch.leaves[0].paths:
                subtotal += sum(
                    [recursive_index(flow_dict, path) for path in leaf_paths]
                )

            res.append(Node(label, subtotal))

            to_add = branch._raw_node_list(flow_dict)
            for i, node_list in enumerate(to_add):
                pos = i + 1
                if len(res) > pos:
                    res.append([])
                res[pos].extend(node_list)

        used = set()
        res = []
        for layer in res:
            res.append([node for node in layer if node.label not in used])
            used |= set(map(lambda n: n.label, layer))

        return res

    def ordered_nodes(self, flow_dict: NestedDict) -> List[List[Node]]:
        """
        Returns a list of node layers where nodes that are shared between parents are
        close together.

        Parameters:
            flow_dict (NestedDict): the dictionary used to create the nodes

        Returns:
            nodes (List[List[Node]]): a list of node layers
        """
        unordered = self._raw_node_list(flow_dict)
        for leaf_list in self.leaves.values():
            if len(leaf_list == 2):
                new_positions = [-1, 0]
                for i, new_pos in enumerate(new_positions):
                    for layer, label in enumerate(leaf_list[0].paths[i]):
                        ind = [
                            i
                            for i, node in enumerate(unordered[layer])
                            if node.label == label
                        ][0]
                        unordered[layer][ind], unordered[layer][new_pos] = (
                            unordered[layer][new_pos],
                            unordered[layer][ind],
                        )

        return unordered

    @staticmethod
    def _get_flows(flow_dict: NestedDict, source: str) -> List[Flow]:
        """
        Returns the list of flows in this tree.
        """
        res = []
        for dest, branch in flow_dict.items():
            res.append(
                Flow(source=source, target=dest, flow_size=dictionary_sum(branch))
            )
            if isinstance(branch, dict):
                res.extend(FlowTree._get_flows(branch, dest))

        return res


def sankey_inputs(flow_dict: NestedDict) -> Tuple[List[List[Node]], List[Flow]]:
    """
    Converts a flow_dictionary to a list of node layers and a list of flows. Tries
    its best to account for multiple leaves having the same label.

    Parameters:
        flow_dict (NestedDict): a nested dictionary of floats

    Returns:
        nodes (List[List[Node]]): a 2D list of node layers
        flows (List[Flow]): a list of flows
    """
    tree = FlowTree.from_flow_dict(flow_dict)

    return FlowTree.ordered_nodes(tree, flow_dict), FlowTree._get_flows(
        flow_dict["Income"], "Income"
    )
