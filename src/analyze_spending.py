from src.visualization_driver import VisualizationDriver
from src.aggregation_driver import AggregationDriver


def analyze_spending():
    """
    Runs the visualization script and performs aggregations.
    """
    VisualizationDriver().visualize()
    AggregationDriver().aggregate()
