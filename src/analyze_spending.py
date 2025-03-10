from datetime import datetime

from src.drivers.visualization_driver import VisualizationDriver
from src.drivers.aggregation_driver import AggregationDriver
from src.drivers.validation_driver import ValidationDriver


def analyze_spending(verbose: bool = True) -> None:
    """
    Runs the visualization script and performs aggregations.

    Parameters:
        verbose (bool): whether to print the time taken. Default is True

    Returns:
        None
    """
    start = datetime.now()
    ValidationDriver().validate_spending()
    VisualizationDriver().visualize()
    AggregationDriver().aggregate()
    if verbose:
        print(
            f"Completed in {round((datetime.now() - start).microseconds / 1e5, 2)}"
            + " seconds."
        )
