from os import getcwd, listdir
from os.path import sep, splitext, abspath, join
from importlib import import_module
from inspect import getmembers, isfunction, getfile

from typing import List, Callable


def get_funcs_from_module(path: str) -> List[Callable]:
    """
    Finds all public functions defined in the Python module
    at `path`. Assumes `path` is domewhere in the cwd.

    Parameters:
        path (str): the path to the module

    Returns:
        funcs (List[Callable]): a list of callable functions
    """
    path_abs = abspath(path)
    raw = splitext(path_abs[len(abspath(getcwd())) :])[0].replace(sep, ".")
    mod_name = raw[int(raw.startswith(".")) : len(raw) - int(raw.endswith("."))]

    return [
        func
        for (name, func) in getmembers(import_module(mod_name), isfunction)
        if not name.startswith("_") and (getfile(func)) == path_abs
    ]


def get_modules_from_folder(dirname: str) -> List[str]:
    """
    Returns the paths to all the valid Python modules in the directory.

    Parameters:
        dirname (str): the name of the directory to search

    Returns:
        paths (List[str]): all the Python modules
    """
    return [
        join(str(dirname), mod)
        for mod in listdir(dirname)
        if splitext(mod)[1] == ".py" and not mod.startswith("_")
    ]
