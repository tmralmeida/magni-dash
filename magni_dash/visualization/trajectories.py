from typing import Dict
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import os
import re


from magni_dash.data_preprocessing.load import load_df
from magni_dash.data_preprocessing.trajectory_data import process_data
from magni_dash.config.constants import TRAJECTORY_SAMPLES_PATH


def load_data(input_file: str):
    raw_df = load_df(
        df_path=os.path.join(TRAJECTORY_SAMPLES_PATH, input_file),
        sep="\t",
        header=11,
        index_col="Frame",
    )
    processed_df = process_data(raw_df=raw_df)
    return processed_df


def play_single_trajectory(input_file: str, processed_df: pd.DataFrame):
    idx_scenario = input_file.find("SC6")
    scenario_name = input_file[idx_scenario: idx_scenario + 4]
    min_frame, max_frame = int(processed_df.index.min()), int(processed_df.index.max())
    slider = st.slider(
        label=f"Frame for {scenario_name}",
        min_value=min_frame,
        max_value=max_frame,
        value=min_frame,
        step=1,
    )
    regex_pattern = re.compile(r"H\d+")
    helmet_number = regex_pattern.findall(input_file)[0][1:]
    fig = px.line(
        processed_df[: slider],
        x=f"Helmet_{helmet_number} - 1 X",
        y=f"Helmet_{helmet_number} - 1 Y",
        title=f"Data from Helmet {helmet_number} in {scenario_name}",
    )
    fig.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        xaxis_range=[
            processed_df[f"Helmet_{helmet_number} - 1 X"].min(),
            processed_df[f"Helmet_{helmet_number} - 1 X"].max(),
        ],
        yaxis_range=[
            processed_df[f"Helmet_{helmet_number} - 1 Y"].min(),
            processed_df[f"Helmet_{helmet_number} - 1 Y"].max(),
        ],
    )
    st.plotly_chart(fig, use_container_width=True)


def play_double_view_trajectories(input_files: Dict, processed_dfs: Dict):
    sliders = {}
    for sc_nm in input_files.keys():
        sliders[sc_nm] = {
            "slider": st.slider(
                label=f"Frame for {sc_nm}",
                min_value=int(processed_dfs[sc_nm].index.min()),
                max_value=int(processed_dfs[sc_nm].index.max()),
                value=int(processed_dfs[sc_nm].index.min()),
                step=1,
            )
        }

    regex_pattern = re.compile(r"H\d+")
    helmet_number = regex_pattern.findall(input_files["SC6A"])[0][1:]

    fig = go.Figure(
        [
            go.Scatter(
                name="SC6A",
                x=processed_dfs["SC6A"].loc[
                    : sliders["SC6A"]["slider"],
                    f"Helmet_{helmet_number} - 1 X",
                ],
                y=processed_dfs["SC6A"].loc[
                    : sliders["SC6A"]["slider"],
                    f"Helmet_{helmet_number} - 1 Y",
                ],
                mode="lines",
                marker=dict(color="blue"),
            ),
            go.Scatter(
                name="SC6B",
                x=processed_dfs["SC6B"].loc[
                    : sliders["SC6B"]["slider"],
                    f"Helmet_{helmet_number} - 1 X",
                ],
                y=processed_dfs["SC6B"].loc[
                    : sliders["SC6B"]["slider"],
                    f"Helmet_{helmet_number} - 1 Y",
                ],
                mode="lines",
                marker=dict(color="red"),
            ),
        ]
    )

    min_x, max_x, min_y, max_y = (
        min(
            processed_dfs["SC6A"][f"Helmet_{helmet_number} - 1 X"].min(),
            processed_dfs["SC6B"][f"Helmet_{helmet_number} - 1 X"].min(),
        ),
        max(
            processed_dfs["SC6A"][f"Helmet_{helmet_number} - 1 X"].max(),
            processed_dfs["SC6B"][f"Helmet_{helmet_number} - 1 X"].max(),
        ),
        min(
            processed_dfs["SC6A"][f"Helmet_{helmet_number} - 1 Y"].min(),
            processed_dfs["SC6B"][f"Helmet_{helmet_number} - 1 Y"].min(),
        ),
        max(
            processed_dfs["SC6A"][f"Helmet_{helmet_number} - 1 Y"].max(),
            processed_dfs["SC6B"][f"Helmet_{helmet_number} - 1 Y"].max(),
        ),
    )

    fig.update_layout(
        title=f"Data from Helmet {helmet_number}",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        xaxis_range=[
            min_x,
            max_x,
        ],
        yaxis_range=[
            min_y,
            max_y,
        ],
    )
    st.plotly_chart(fig, use_container_width=True)
