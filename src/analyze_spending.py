from datetime import datetime

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
    start = datetime.now()
    VisualizationDriver().visualize()
    AggregationDriver().aggregate()
    print(f"Completed in {round((datetime.now() - start).microseconds / 1e5, 2)} seconds.")
