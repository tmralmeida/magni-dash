import streamlit as st
import pandas as pd


def run_configs(scenario_id: int):
    """set configs of a page"""
    st.set_page_config(page_title=f"Scenario {scenario_id}", layout="wide")
    st.sidebar.header(f"Scenario {scenario_id}")
    st.markdown(f"# Scenario {scenario_id}")


def interpolate_with_rule(
    input_df: pd.DataFrame, column_name: str, max_consecutive_nans: int
):
    """Interpolate trajectories given a max number of NaN values"""
    mask = input_df[column_name].isna()
    groups = mask.ne(mask.shift()).cumsum()
    interpolated_column = input_df[column_name].interpolate(method="linear")
    interpolated_column = interpolated_column.where(
        groups.groupby(groups).transform("size") <= max_consecutive_nans,
        input_df[column_name],
    )
    input_df[column_name] = interpolated_column
    return input_df
