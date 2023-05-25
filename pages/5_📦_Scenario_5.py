import os
import pandas as pd
import streamlit as st

from st_components.common import run_configs
from st_components.cache import (
    preprocess_df,
    transform_df2plotly,
    get_best_markers,
    extract_features,
    filter_best_markers,
)
from utils.common import GroupsInfo
from visualization.multi_trajectory import (
    get_multi_element_trajectories,
    get_eyt_trajectories_visualization,
)
from config.constants import TRAJECTORY_SAMPLES_PATH


SCENARIO5_PATH = os.path.join(TRAJECTORY_SAMPLES_PATH, "Scenario5")


run_configs(scenario_id=5)
with st.expander("See description"):
    st.write(
        """
            In Scenario 5, one participant was performing as a worker in a factory carrying
            objects between two points in the environment. The robot (remotely controlled by one of
            us) proactively offers help to the participant. If the participant accepted, the robot
            would ask to place the objects on top of it. Otherwise, the participant was asked to
            continue with the task.
            """
    )

files = os.listdir(SCENARIO5_PATH)
files_target = list(filter(lambda x: x.endswith(".csv"), files))

input_file = st.sidebar.selectbox(
    label="File", options=files_target, key="input_file", label_visibility="visible"
)

if st.session_state.input_file:
    tab_trajectories, tab_eyt_sync3d = st.tabs(["2D Trajectory data", "Eyetracking"])

    df_path = os.path.join(SCENARIO5_PATH, input_file)
    raw_df = pd.read_csv(df_path, index_col="Frame")
    best_markers_counter = get_best_markers(input_df=raw_df)
    preprocessed_df = preprocess_df(raw_df.copy())
    moving_agents = preprocessed_df.columns[
        (preprocessed_df.columns.str.startswith("Helmet"))
        | (preprocessed_df.columns.str.startswith("LO1"))
    ].tolist()
    moving_agents_labels = set(map(lambda x: x.split(" - ")[0], moving_agents))
    moving_agents_labels = list(filter(
        lambda x: len(x.split(" ")) == 1, moving_agents_labels
    ))

    moving_agents_cols = preprocessed_df.columns[
        (preprocessed_df.columns.str.endswith(" X"))
        | ((preprocessed_df.columns.str.endswith(" Y")))
        | ((preprocessed_df.columns.str.endswith(" Z")))
    ]
    features_df = extract_features(
        preprocessed_df[["Time"] + moving_agents_cols.tolist()].copy(),
        magents_labels=moving_agents_labels,
        darko_label="DARKO_Robot",
    )
    features_df.index = features_df["Frame"]
    features_cat = preprocessed_df.join(features_df)
    rotations_cols = features_cat[
        features_cat.columns[features_cat.columns.str.contains(r"R(\d)")]
    ].columns.tolist()
    features_filtered = features_cat[
        features_cat.columns[
            (features_cat.columns.str.endswith("X"))
            | (features_cat.columns.str.endswith("Y"))
            | (features_cat.columns.str.endswith("Z"))
            | (features_cat.columns.str.endswith("speed (m/s)"))
        ].tolist()
        + rotations_cols
    ]
    darko_info = GroupsInfo(
        element_id="DARKO_Robot",
        markers_pattern_re=r"DARKO_Robot - (\d).*",
        label_sep=" - ",
    )
    helmets_info = GroupsInfo(
        element_id="Helmet",
        markers_pattern_re=r"Helmet_(\d+ - \d).*",
        label_sep="_",
    )
    tobii_info = GroupsInfo(
        element_id="Helmet",
        markers_pattern_re=r"Helmet_(\d+ TB\d)_G3D.*",
        label_sep="_",
    )
    centroids_info = GroupsInfo(
        element_id="Helmet",
        markers_pattern_re=r"Helmet_(\d+) Centroid_.*",
        label_sep="_",
    )
    rotations_info = GroupsInfo(
        element_id="Helmet",
        markers_pattern_re=r"Helmet_(\d+) R.*",
        label_sep="_",
    )
    trajectories_df_plot = transform_df2plotly(
        input_df=features_filtered.copy(),
        groups_info=[helmets_info, darko_info],
    )
    transformed_tobii = transform_df2plotly(
        input_df=features_filtered.copy(),
        groups_info=[tobii_info],
    )
    transformed_centroids = transform_df2plotly(
        input_df=features_filtered.copy(),
        groups_info=[centroids_info],
    )
    transformed_rotations = transform_df2plotly(
        input_df=features_filtered.copy(),
        groups_info=[rotations_info],
    )
    transformed_eyt = transformed_tobii.sort_index()
    transformed_centroids = transformed_centroids.sort_index().drop("eid", axis=1)
    transformed_rotations = transformed_rotations.sort_index()
    cent_rot = pd.concat([transformed_centroids, transformed_rotations], axis=1)
    best_makers_df = filter_best_markers(
        elements_cat_df=trajectories_df_plot.copy(),
        nan_counter_by_marker=best_markers_counter,
    )
    with tab_trajectories:
        figs = get_multi_element_trajectories(best_makers_df)
        for fig in figs:
            st.plotly_chart(fig, use_container_width=True)
    with tab_eyt_sync3d:
        fig = get_eyt_trajectories_visualization(
            best_makers_df, transformed_eyt, cent_rot
        )
        st.plotly_chart(fig, use_container_width=True)
