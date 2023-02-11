from typing import Optional
import pandas as pd
from magni_dash.config.constants import TRAJECTORY_DATA_TYPE


def process_data(
    raw_df: pd.DataFrame, height_suffix: Optional[str] = "Z"
) -> pd.DataFrame:
    """Process raw trajectories data
    1) Remove third dimension column
    2) Remove columns with all NaNs values

    Parameters
    ----------
    df
        Raw pandas DataFrame.
    height_suffix, optional
        Suffix used in the thrid dimension column, by default "Z"

    Returns
    -------
        DataFrame with the third dimension column removed.
    """
    df_out = raw_df.copy()
    if TRAJECTORY_DATA_TYPE == "2D":
        df_out = raw_df[raw_df.columns[~raw_df.columns.str.endswith(height_suffix)]]
    df_out = df_out.dropna(axis=1, how="all")
    df_out = df_out.interpolate()
    return df_out
