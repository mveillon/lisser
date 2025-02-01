from src.visualization_driver import VisualizationDriver
from src.aggregation_driver import AggregationDriver


def analyze_spending() -> None:
    """
    Runs the visualization script and performs aggregations.

    Parameters:
        None

    Returns:
        None
    """
    VisualizationDriver().visualize()
    AggregationDriver().aggregate()
