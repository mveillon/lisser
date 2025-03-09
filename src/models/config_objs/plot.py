from typing import Literal, List

from src.utilities.decorators import dataclass_from_converted_json
from src.models.config_objs.line import Line


@dataclass_from_converted_json(
    converters={"lines": lambda lst: list(map(Line, lst))}  # type: ignore
)
class Plot:
    """
    One plot to generate.

    Attributes:
        plot_name (str): the name of the file that will contain this graph
        title (str): the title at the top of the graph
        timeframe (str): over what timeframe to aggregate the data. Either "yearly"
            or "monthly"
        lines (List[Line]): a list of lines to include in the plot
    """

    plot_name: str
    title: str
    timeframe: Literal["yearly", "monthly"]
    lines: List[Line]
