import os
import streamlit as st
import pandas as pd

from magni_dash.st_components.common import run_configs
from magni_dash.st_components.cache import (
    # load_df,
    preprocess_df,
    transform_df2plotly,
    get_best_markers,
    extract_features,
    filter_best_markers,
)
from magni_dash.utils.common import GroupsInfo
from magni_dash.visualization.multi_trajectory import (
    get_multi_element_trajectories,
    get_eyt_trajectories_visualization,
)
from magni_dash.config.constants import TRAJECTORY_SAMPLES_PATH


SCENARIO3_PATH = os.path.join(TRAJECTORY_SAMPLES_PATH, "Scenario3")


run_configs(scenario_id=3)
with st.expander("See description"):
    st.write(
        """
            Scenario 3 has two variations: 3A, in
            which the teleoperated robot moves as a regular differential
            drive robot, and 3B, where the robot moves in an omnidirectional way.
            In both cases, an operator drives the mobile
            robot using a remote controller.
            """
    )

files = os.listdir(SCENARIO3_PATH)
files_target = list(filter(lambda x: x.endswith("merged.csv"), files))

input_file = st.sidebar.selectbox(
    label="File", options=files_target, key="input_file", label_visibility="visible"
)
if st.session_state.input_file:
    tab_trajectories, tab_eyt_sync3d = st.tabs(["2D Trajectory data", "EYT data"])

    df_path = os.path.join(SCENARIO3_PATH, input_file)
    # raw_df = load_df(
    #     df_path=df_path,
    #     header=11,
    #     sep="\t",
    #     index_col="Frame",
    # )
    raw_df = pd.read_csv(df_path, index_col="Frame")
    best_markers_counter = get_best_markers(input_df=raw_df)
    preprocessed_df = preprocess_df(raw_df.copy())
    moving_agents = preprocessed_df.columns[
        (preprocessed_df.columns.str.startswith("Helmet"))
        | (preprocessed_df.columns.str.startswith("LO1"))
    ].tolist()
    # moving_agents_labels = set(map(lambda x: x.split(" - ")[0], moving_agents))
    moving_agents_labels = set(map(lambda x: x.split(" - ")[0], moving_agents))
    moving_agents_labels = filter(
        lambda x: len(x.split(" ")) == 1, moving_agents_labels
    )

    # features_df = extract_features(
    #     preprocessed_df.copy(),
    #     magents_labels=list(moving_agents_labels),
    #     darko_label="DARKO",
    # )
    moving_agents_cols = preprocessed_df.columns[
        (preprocessed_df.columns.str.endswith(" X"))
        | ((preprocessed_df.columns.str.endswith(" Y")))
        | ((preprocessed_df.columns.str.endswith(" Z")))
    ]
    features_df = extract_features(
        preprocessed_df[["Time"] + moving_agents_cols.tolist()].copy(),
        magents_labels=list(moving_agents_labels),
        darko_label="DARKO",
    )
    features_cat = preprocessed_df.join(features_df)
    features_filtered = features_cat[
        features_cat.columns[
            (features_cat.columns.str.endswith("X"))
            | (features_cat.columns.str.endswith("Y"))
            | (features_cat.columns.str.endswith("Z"))
            | (features_cat.columns.str.endswith("speed (m/s)"))
        ]
    ]
    # features_filtered = features_cat[
    #     features_cat.columns[
    #         (features_cat.columns.str.endswith("X"))
    #         | (features_cat.columns.str.endswith("Y"))
    #         | (features_cat.columns.str.endswith("speed (m/s)"))
    #     ]
    # ]
    lo_info = GroupsInfo(
        element_id="LO1", markers_pattern_re=r"LO1 - (\d).*", label_sep=" - "
    )
    darko_info = GroupsInfo(
        element_id="DARKO", markers_pattern_re=r"DARKO - (\d).*", label_sep=" - "
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
    trajectories_df_plot = transform_df2plotly(
        input_df=features_filtered.copy(),
        groups_info=[helmets_info, darko_info, lo_info],
    )
    transformed_tobii = transform_df2plotly(
        input_df=features_filtered.copy(),
        groups_info=[tobii_info],
    )
    transformed_centroids = transform_df2plotly(
        input_df=features_filtered.copy(),
        groups_info=[centroids_info],
    )
    transformed_eyt = transformed_tobii.sort_index()
    transformed_centroids = transformed_centroids.sort_index()
    best_makers_df = filter_best_markers(
        elements_cat_df=trajectories_df_plot.copy(),
        nan_counter_by_marker=best_markers_counter,
    )
    with tab_trajectories:
        figs = get_multi_element_trajectories(best_makers_df)
        for fig in figs:
            st.plotly_chart(fig, use_container_width=True)
    with tab_eyt_sync3d:
        st.write("wip")
        fig = get_eyt_trajectories_visualization(
            best_makers_df, transformed_eyt, transformed_centroids
        )
        st.plotly_chart(fig, use_container_width=True)
