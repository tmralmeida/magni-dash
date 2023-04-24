import pandas as pd
import plotly.express as px
import streamlit as st


def get_multi_element_trajectories(input_df: pd.DataFrame):
    min_frame, max_frame = int(input_df.Frame.min()), int(input_df.Frame.max())
    slider = st.slider(
        label="Frame",
        min_value=min_frame,
        max_value=max_frame,
        value=(min_frame, min_frame + 10),
        step=1,
        key="slider_scenario1",
    )

    fig = px.line(
        input_df[(input_df.Frame >= slider[0]) & (input_df.Frame <= slider[1])],
        x="X (m)",
        y="Y (m)",
        color="eid",
    )
    fig.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        margin=dict(l=0, r=0, t=20, b=20),
    )
    figs = [fig]
    if "speed (m/s)" in input_df.columns:
        speed_fig = px.line(
            input_df[(input_df.Frame >= slider[0]) & (input_df.Frame <= slider[1])],
            x="Frame",
            y="speed (m/s)",
            color="eid",
        )
        figs += [speed_fig]
    return figs
