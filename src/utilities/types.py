import pandas as pd
from typing import Union, Dict, Any, Callable

Number = Union[int, float]
NestedDict = Union[Number, Dict[str, "NestedDict"]]
OperatorFunction = Callable[[pd.Series, Any], pd.Series]
Plotter = Callable[[pd.DataFrame, str], None]
