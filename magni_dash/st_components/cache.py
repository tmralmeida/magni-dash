import streamlit as st
import pandas as pd

from magni_dash.data_preprocessing.spatio_temporal_features import (
    SpatioTemporalFeatures,
)
from magni_dash.config.constants import TRAJECTORY_DATA_TYPE


@st.cache_data
def load_df(df_path: str, sep: str, header: int, index_col: str):
    """Load a csv pandas dataframe.

    Parameters
    ----------
    df_path
        Absolute path to the file.
    sep
        Separation marker.
    header
        Header rows size.
    index_col
        Column name for the index.

    Returns
    -------
        Pandas DtaFrame object.
    """
    return pd.read_csv(
        df_path,
        sep=sep,
        header=header,
        index_col=index_col,
    )


@st.cache_data
def process_data(raw_df: pd.DataFrame, height_suffix: str = "Z") -> pd.DataFrame:
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


@st.cache_data
def extract_features(input_df: pd.DataFrame, helmet_number: str):
    out_df = input_df.copy()
    out_df[
        out_df.columns[
            (out_df.columns.str.startswith("DARKO_Robot"))
            | (out_df.columns.str.startswith("Helmet"))
        ]
    ] /= 1000
    out_df = SpatioTemporalFeatures.get_speed(
        out_df,
        time_col_name="Time",
        element_name=[f"Helmet_{helmet_number}", "DARKO_robot"],
    )

    out_df = out_df.reset_index()
    return out_df
