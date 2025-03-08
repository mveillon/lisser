import pandas as pd

def empty_dataframe(df: pd.DataFrame) -> None:
    """
    Checks that df isn't empty.

    Parameters:
        df (DataFrame): the DataFrame to validate

    Returns:
        None
    """
    if df.shape[0] == 0:
        raise ValueError("Validation error: empty spreadsheet.")