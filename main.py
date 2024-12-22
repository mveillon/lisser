from src.visualization_driver import VisualizationDriver
from src.aggregation_driver import AggregationDriver


def run():
    """
    Runs the visualization script and performs aggregations.
    """
    VisualizationDriver().visualize()
    AggregationDriver().aggregate()


if __name__ == "__main__":
    run()
