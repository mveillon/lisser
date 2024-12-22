from dataclasses import dataclass
from typing import List

from src.read_config.filter import Filter


@dataclass
class Line:
    """
    A line in a plot, summing the total amount spent over a period of time.

    Attributes:
        filters (List[Filter]): what filters to apply to draw this line
        style (str): how to style the line, according to matplotlib rules
        label (str): the label of the line in the legend. If empty, will not
            appear in the legend, which will only be there if at least one
            line has a label.
        disjunction (bool): whether to combine the filters using OR instead
            of AND. Default is False
    """

    filters: List[Filter]
    style: str = "b"
    label: str = ""
    disjunction: bool = False
