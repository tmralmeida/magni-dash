import pandas as pd
import numpy as np
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
    X_COORD = (1.0, 0, 0)
    Y_COORD = (0, 1.0, 0)
    Z_COORD = (0, 0, 1.0)
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
        centroids = target_centroids[target_centroids["eid"] == eid]
        rotations = centroids[
            centroids.columns[centroids.columns.str.contains("R")]
        ].iloc[-1]
        rotations_reshaped = rotations.values.reshape(3, 3).T
        x_rep = np.array([[1.0, 0, 0]])
        y_rep = np.array([[0, 1.0, 0]])
        z_rep = np.array([[0, 0, 1.0]])
        x_rotated = np.matmul(x_rep, rotations_reshaped).squeeze()
        y_rotated = np.matmul(y_rep, rotations_reshaped).squeeze()
        z_rotated = np.matmul(z_rep, rotations_reshaped).squeeze()
        initial_pt = (
            centroids[centroids.Frame == slider[1]][
                ["Centroid X (m)", "Centroid Y (m)", "Centroid Z (m)"]
            ].values
            / 1000
        ).squeeze()
        x_trans = x_rotated + initial_pt
        y_trans = y_rotated + initial_pt
        z_trans = z_rotated + initial_pt

        eyt_data = target_eyt[target_eyt["eid"] == eid]
        trace_trajs = go.Scatter3d(
            x=trajectories["X (m)"],
            y=trajectories["Y (m)"],
            z=trajectories["Z (m)"],
            mode="lines",
            name=eid,
        )

        trace_centroids_x = go.Scatter3d(
            x=[initial_pt[0], x_trans[0], None],
            y=[initial_pt[1], x_trans[1], None],
            z=[initial_pt[2], x_trans[2], None],
            mode="lines",
            line=dict(color="red", width=5),
            showlegend=False,
        )
        trace_centroids_y = go.Scatter3d(
            x=[initial_pt[0], y_trans[0], None],
            y=[initial_pt[1], y_trans[1], None],
            z=[initial_pt[2], y_trans[2], None],
            mode="lines",
            line=dict(color="green", width=5),
            showlegend=False,
        )
        trace_centroids_z = go.Scatter3d(
            x=[initial_pt[0], z_trans[0], None],
            y=[initial_pt[1], z_trans[1], None],
            z=[initial_pt[2], z_trans[2], None],
            mode="lines",
            line=dict(color="blue", width=5),
            showlegend=False,
        )
        gaze_x, gaze_y, gaze_z = (
            eyt_data[["TB_G3D X (m)", "TB_G3D Y (m)", "TB_G3D Z (m)"]].iloc[-1] / 1000
        )
        trace_gaze = go.Scatter3d(
            x=[initial_pt[0], gaze_x, None],
            y=[initial_pt[1], gaze_y, None],
            z=[initial_pt[2], gaze_z, None],
            mode="lines",
            line=dict(color="orange", width=5),
            showlegend=False,
        )
        fig.add_trace(trace_trajs)
        fig.add_trace(trace_centroids_x)
        fig.add_trace(trace_centroids_y)
        fig.add_trace(trace_centroids_z)
        fig.add_trace(trace_gaze)

    fig = add_reference_frame(fig, ORIGIN, X_COORD, Y_COORD, Z_COORD)

    fig.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        margin=dict(l=20, r=20, t=20, b=20),
        scene=dict(
            xaxis_title="X (m)",
            yaxis_title="Y (m)",
            zaxis_title="Z (m)",
            aspectmode="data",
        ),
    )
    return fig
