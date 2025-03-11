import pandas as pd
import tkinter as tk
from typing import Union, Dict, Any, Callable

Number = Union[int, float]
NestedDict = Union[Number, Dict[str, "NestedDict"]]
OperatorFunction = Callable[[pd.Series, Any], pd.Series]
Plotter = Callable[[pd.DataFrame, str], None]
Root = Union[tk.Tk, tk.Frame]
