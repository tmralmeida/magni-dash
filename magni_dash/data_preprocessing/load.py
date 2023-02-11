import streamlit as st
import pandas as pd


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
