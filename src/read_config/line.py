from typing import List, Optional

from src.read_config.filter import Filter
from src.read_config.agg_function import AggFunction
from src.utilities.decorators import dataclass_from_json


@dataclass_from_json({"filters": Filter})
class Line:
    """
    A line in a plot, summing the total amount spent over a period of time.

    Attributes:
        filters (List[Filter]): what filters to apply to draw this line
        agg (Optional[AggFunction]): a function used to aggregate the line. In
            the config file, this is a list of aggregations, but the list is
            exploded so there is just one function per line
        style (str): how to style the line, according to matplotlib rules
        label (str): the label of the line in the legend. If empty, will not
            appear in the legend, which will only be there if at least one
            line has a label
        disjunction (bool): whether to combine the filters using OR instead
            of AND. Default is False
    """

    filters: List[Filter]
    agg: Optional[AggFunction] = None
    style: str = "b"
    label: str = ""
    disjunction: bool = False
