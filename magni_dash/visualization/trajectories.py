import re
from typing import Dict, Optional
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st


def get_single_trajectory(
    helmet_number: str,
    marker: str,
    input_file: str,
    processed_df: pd.DataFrame,
    tab_component,
    features_df: Optional[pd.DataFrame] = None,
):
    idx_scenario = input_file.find("SC6")
    scenario_name = input_file[idx_scenario : idx_scenario + 4]
    min_frame, max_frame = int(processed_df.index.min()), int(processed_df.index.max())
    slider = tab_component.slider(
        label=f"Frame for {scenario_name}",
        min_value=min_frame,
        max_value=max_frame,
        value=min_frame,
        step=1,
        key=input_file,
    )

    fig = px.line(
        processed_df[:slider],
        x=f"Helmet_{helmet_number} - {marker} X",
        y=f"Helmet_{helmet_number} - {marker} Y",
        title=f"Trajectory data from Helmet {helmet_number} in {scenario_name}",
    )
    fig.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        xaxis_range=[
            processed_df[f"Helmet_{helmet_number} - {marker} X"].min(),
            processed_df[f"Helmet_{helmet_number} - {marker} X"].max(),
        ],
        yaxis_range=[
            processed_df[f"Helmet_{helmet_number} - {marker} Y"].min(),
            processed_df[f"Helmet_{helmet_number} - {marker} Y"].max(),
        ],
    )
    figs = [fig]
    if features_df is not None:
        fig_speed = px.line(
            features_df[:slider],
            x="Frame",
            y=f"speed_Helmet_{helmet_number}-{marker} (m/s)",
            title=f"Speed profile from Helmet {helmet_number} in {scenario_name}",
        )
        figs += [fig_speed]

    return figs


def get_double_overlayed_view(
    inputs_specfications: Dict,
    marker,
):
    trajectory_dfa = inputs_specfications["SC6A"].trajectory_df
    trajectory_dfb = inputs_specfications["SC6B"].trajectory_df

    slider_min_value = min(
        int(trajectory_dfa.index.min()), int(trajectory_dfb.index.min())
    )
    slider_max_value = max(
        int(trajectory_dfa.index.max()), int(trajectory_dfb.index.max())
    )

    slider = st.slider(
        label="Frame",
        min_value=slider_min_value,
        max_value=slider_max_value,
        value=slider_min_value,
        step=1,
        key="slider_overlayed",
    )

    regex_pattern = re.compile(r"H\d+")
    helmet_number = regex_pattern.findall(inputs_specfications["SC6A"].input_file)[0][
        1:
    ]

    fig = go.Figure(
        [
            go.Scatter(
                name="SC6A",
                x=trajectory_dfa.loc[
                    : min(slider, int(trajectory_dfa.index.max())),
                    f"Helmet_{helmet_number} - {marker} X",
                ],
                y=trajectory_dfa.loc[
                    : min(slider, int(trajectory_dfa.index.max())),
                    f"Helmet_{helmet_number} - {marker} Y",
                ],
                mode="lines",
                marker=dict(color="blue"),
            ),
            go.Scatter(
                name="SC6B",
                x=trajectory_dfb.loc[
                    : min(slider, int(trajectory_dfb.index.max())),
                    f"Helmet_{helmet_number} - {marker} X",
                ],
                y=trajectory_dfb.loc[
                    : min(slider, int(trajectory_dfb.index.max())),
                    f"Helmet_{helmet_number} - {marker} Y",
                ],
                mode="lines",
                marker=dict(color="red"),
            ),
        ]
    )

    min_x, max_x, min_y, max_y = (
        min(
            trajectory_dfa[f"Helmet_{helmet_number} - {marker} X"].min(),
            trajectory_dfb[f"Helmet_{helmet_number} - {marker} X"].min(),
        ),
        max(
            trajectory_dfa[f"Helmet_{helmet_number} - {marker} X"].max(),
            trajectory_dfb[f"Helmet_{helmet_number} - {marker} X"].max(),
        ),
        min(
            trajectory_dfa[f"Helmet_{helmet_number} - {marker} Y"].min(),
            trajectory_dfb[f"Helmet_{helmet_number} - {marker} Y"].min(),
        ),
        max(
            trajectory_dfa[f"Helmet_{helmet_number} - {marker} Y"].max(),
            trajectory_dfb[f"Helmet_{helmet_number} - {marker} Y"].max(),
        ),
    )

    fig.update_layout(
        title=f"Trajectory data from Helmet {helmet_number}",
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
    figs = [fig]

    features_df_a = inputs_specfications["SC6A"].features_df
    features_df_b = inputs_specfications["SC6B"].features_df
    if features_df_a is not None and features_df_b is not None:
        features_df_a["Scenario"] = "6A"
        features_df_b["Scenario"] = "6B"
        features_df = pd.concat([features_df_a, features_df_b], axis=0)
        features_df = features_df.sort_index()
        fig_speed = px.line(
            features_df[:slider],
            x="Frame",
            y=f"speed_Helmet_{helmet_number}-{marker} (m/s)",
            color="Scenario",
            title=f"Speed profile from Helmet {helmet_number} ",
            color_discrete_sequence=["blue", "red"]
        )
        figs += [fig_speed]
    return figs
