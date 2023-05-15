import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go


def get_multi_element_trajectories(input_df: pd.DataFrame):
    min_frame, max_frame = int(input_df.Frame.min()), int(input_df.Frame.max())
    slider = st.slider(
        label="Frame",
        min_value=min_frame,
        max_value=max_frame,
        value=(min_frame, min_frame + 10),
        step=1,
        key="slider_scenario",
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


def add_reference_frame(fig, origin, x_coord, y_coord, z_coord):
    fig.add_trace(
        go.Scatter3d(
            x=[origin[0], x_coord[0], None],
            y=[origin[1], x_coord[1], None],
            z=[origin[2], x_coord[2], None],
            mode="lines",
            line=dict(color="red", width=5),
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Scatter3d(
            x=[origin[0], y_coord[0], None],
            y=[origin[1], y_coord[1], None],
            z=[origin[2], y_coord[2], None],
            mode="lines",
            line=dict(color="green", width=5),
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Scatter3d(
            x=[origin[0], z_coord[0], None],
            y=[origin[1], z_coord[1], None],
            z=[origin[2], z_coord[2], None],
            mode="lines",
            line=dict(color="blue", width=5),
            showlegend=False,
        )
    )

    fig.add_cone(
        x=[x_coord[0]],
        y=[0],
        z=[0],
        u=[x_coord[0]],
        v=[0],
        w=[0],
        colorscale=[[0, "red"], [1, "red"]],
        showscale=False,
    )

    fig.add_cone(
        x=[0],
        y=[y_coord[1]],
        z=[0],
        u=[0],
        v=[y_coord[1]],
        w=[0],
        colorscale=[[0, "green"], [1, "green"]],
        showscale=False,
    )

    fig.add_cone(
        x=[0],
        y=[0],
        z=[z_coord[2]],
        u=[0],
        v=[0],
        w=[z_coord[2]],
        colorscale=[[0, "blue"], [1, "blue"]],
        showscale=False,
    )
    return fig


def get_eyt_trajectories_visualization(
    trajectories_df: pd.DataFrame, eyt_df: pd.DataFrame, centroids_df: pd.DataFrame
):
    eyt_df["Frame"] = eyt_df.index
    centroids_df["Frame"] = centroids_df.index
    ORIGIN = (0, 0, 0)
    X_COORD = (2.0, 0, 0)
    Y_COORD = (0, 0.5, 0)
    Z_COORD = (0, 0, 0.25)
    min_frame, max_frame = int(trajectories_df.Frame.min()), int(
        trajectories_df.Frame.max()
    )
    slider = st.slider(
        label="Frame",
        min_value=min_frame,
        max_value=max_frame,
        value=(min_frame, min_frame + 10),
        step=1,
        key="slider_eyt",
    )
    target_trajectories = trajectories_df[
        (trajectories_df.Frame >= slider[0]) & (trajectories_df.Frame <= slider[1])
    ]
    target_centroids = centroids_df[
        (centroids_df.Frame >= slider[0]) & (centroids_df.Frame <= slider[1])
    ]
    target_eyt = eyt_df[(eyt_df.Frame >= slider[0]) & (eyt_df.Frame <= slider[1])]
    fig = go.Figure()
    for eid in eyt_df.eid.unique():
        trajectories = target_trajectories[target_trajectories["eid"] == eid]
        centroids_data = target_centroids[target_centroids["eid"] == eid]
        eyt_data = target_eyt[target_eyt["eid"] == eid]
        trace_trajs = go.Scatter3d(
            x=trajectories["X (m)"],
            y=trajectories["Y (m)"],
            z=trajectories["Z (m)"],
            mode="lines",
            name=eid,
        )
        trace_centroids = go.Scatter3d(
            x=centroids_data[centroids_data.Frame == slider[1]]["Centroid X (m)"]
            / 1000,
            y=centroids_data[centroids_data.Frame == slider[1]]["Centroid Y (m)"]
            / 1000,
            z=centroids_data[centroids_data.Frame == slider[1]]["Centroid Z (m)"]
            / 1000,
            mode="markers",
            name=f"{eid} RF",
        )
        trace_eyt = go.Scatter3d(
            x=eyt_data["TB_G3D X (m)"],
            y=eyt_data["TB_G3D Y (m)"],
            z=eyt_data["TB_G3D Z (m)"],
            mode="markers",
            name=f"Gaze point from {eid}",
        )
        fig.add_trace(trace_trajs)
        fig.add_trace(trace_centroids)
        fig.add_trace(trace_eyt)

    fig = add_reference_frame(fig, ORIGIN, X_COORD, Y_COORD, Z_COORD)

    fig.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        margin=dict(l=0, r=0, t=10, b=0),
        scene=dict(
            xaxis_title="X (m)",
            yaxis_title="Y (m)",
            zaxis_title="Z (m)",
            xaxis=dict(range=[trajectories_df["X (m)"].min(), trajectories_df["X (m)"].max()]),
            yaxis=dict(range=[trajectories_df["Y (m)"].min(), trajectories_df["Y (m)"].max()]),
            zaxis=dict(range=[trajectories_df["Z (m)"].min(), trajectories_df["Z (m)"].max()]),
        ),
    )
    return fig
