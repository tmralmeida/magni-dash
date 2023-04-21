from typing import Dict, Optional
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st


def get_single_trajectory(
    helmet_label: str,
    marker: str,
    input_file: str,
    processed_df: pd.DataFrame,
    tab_component,
    features_df: Optional[pd.DataFrame] = None,
):
    idx_scenario = input_file.find("SC6")
    scenario_name = input_file[idx_scenario: idx_scenario + 4]
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
        x=f"{helmet_label} - {marker} X",
        y=f"{helmet_label} - {marker} Y",
        title=f"Trajectory data from {helmet_label} in {scenario_name}",
    )
    fig.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        xaxis_range=[
            processed_df[f"{helmet_label} - {marker} X"].min(),
            processed_df[f"{helmet_label} - {marker} X"].max(),
        ],
        yaxis_range=[
            processed_df[f"{helmet_label} - {marker} Y"].min(),
            processed_df[f"{helmet_label} - {marker} Y"].max(),
        ],
        margin=dict(l=0, r=0, t=20, b=20),
    )
    figs = [fig]
    if features_df is not None:
        fig_speed = px.line(
            features_df[:slider],
            x="Frame",
            y=f"{helmet_label} - {marker} speed (m/s)",
            title=f"Speed profile from {helmet_label} in {scenario_name}",
        )
        figs += [fig_speed]

    return figs


def get_double_overlayed_view(
    inputs_specfications: Dict,
    marker,
):
    helmet_label = inputs_specfications["SC6A"].helmet_label
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

    fig = go.Figure(
        [
            go.Scatter(
                name="SC6A",
                x=trajectory_dfa.loc[
                    : min(slider, int(trajectory_dfa.index.max())),
                    f"{helmet_label} - {marker} X",
                ],
                y=trajectory_dfa.loc[
                    : min(slider, int(trajectory_dfa.index.max())),
                    f"{helmet_label} - {marker} Y",
                ],
                mode="lines",
                marker=dict(color="blue"),
            ),
            go.Scatter(
                name="SC6B",
                x=trajectory_dfb.loc[
                    : min(slider, int(trajectory_dfb.index.max())),
                    f"{helmet_label} - {marker} X",
                ],
                y=trajectory_dfb.loc[
                    : min(slider, int(trajectory_dfb.index.max())),
                    f"{helmet_label} - {marker} Y",
                ],
                mode="lines",
                marker=dict(color="red"),
            ),
        ]
    )
    fig.update_layout(margin=dict(l=0, r=0, t=20, b=20))

    min_x, max_x, min_y, max_y = (
        min(
            trajectory_dfa[f"{helmet_label} - {marker} X"].min(),
            trajectory_dfb[f"{helmet_label} - {marker} X"].min(),
        ),
        max(
            trajectory_dfa[f"{helmet_label} - {marker} X"].max(),
            trajectory_dfb[f"{helmet_label} - {marker} X"].max(),
        ),
        min(
            trajectory_dfa[f"{helmet_label} - {marker} Y"].min(),
            trajectory_dfb[f"{helmet_label} - {marker} Y"].min(),
        ),
        max(
            trajectory_dfa[f"{helmet_label} - {marker} Y"].max(),
            trajectory_dfb[f"{helmet_label} - {marker} Y"].max(),
        ),
    )

    fig.update_layout(
        title=f"Trajectory data from {helmet_label}",
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

    no_ex_cols = set(features_df_a.columns).difference(set(features_df_b.columns))
    if len(no_ex_cols) > 0:
        st.error(
            "Speed profile not available. Probably, trajectory data with misclassifications!",
            icon="🚨",
        )
        return figs

    if features_df_a is None or features_df_b is None:
        return figs

    features_df_a["Scenario"] = "6A"
    features_df_b["Scenario"] = "6B"
    features_df = pd.concat([features_df_a, features_df_b], axis=0)
    features_df = features_df.sort_index()
    fig_speed = px.line(
        features_df[:slider],
        x="Frame",
        y=f"{helmet_label} - {marker} speed (m/s)",
        color="Scenario",
        title=f"Speed profile from {helmet_label}",
        color_discrete_sequence=["blue", "red"],
    )
    figs += [fig_speed]
    return figs
