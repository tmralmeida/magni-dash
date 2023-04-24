import os
import streamlit as st

from magni_dash.st_components.common import run_configs
from magni_dash.st_components.cache import (
    load_df,
    preprocess_df,
    transform_df2plotly,
    get_best_markers,
    extract_features,
    filter_best_markers,
)
from magni_dash.utils.common import GroupsInfo
from magni_dash.visualization.multi_trajectory import get_multi_element_trajectories
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
files_target = list(filter(lambda x: x.endswith("pp.tsv"), files))

input_file = st.sidebar.selectbox(
    label="File", options=files_target, key="input_file", label_visibility="visible"
)
if st.session_state.input_file:
    df_path = os.path.join(SCENARIO3_PATH, input_file)
    raw_df = load_df(
        df_path=df_path,
        header=11,
        sep="\t",
        index_col="Frame",
    )
    best_markers_counter = get_best_markers(input_df=raw_df)
    preprocessed_df = preprocess_df(raw_df.copy())
    moving_agents = preprocessed_df.columns[
        (preprocessed_df.columns.str.startswith("Helmet"))
        | (preprocessed_df.columns.str.startswith("LO1"))
    ].tolist()
    moving_agents_labels = set(map(lambda x: x.split(" - ")[0], moving_agents))
    features_df = extract_features(
        preprocessed_df.copy(),
        magents_labels=list(moving_agents_labels),
        darko_label="DARKO",
    )
    features_cat = preprocessed_df.join(features_df)
    features_filtered = features_cat[
        features_cat.columns[
            (features_cat.columns.str.endswith("X"))
            | (features_cat.columns.str.endswith("Y"))
            | (features_cat.columns.str.endswith("speed (m/s)"))
        ]
    ]
    lo_info = GroupsInfo(
        element_id="LO1", markers_pattern_re=r"LO1 - (\d).*", label_sep=" - "
    )
    darko_info = GroupsInfo(
        element_id="DARKO", markers_pattern_re=r"DARKO - (\d).*", label_sep=" - "
    )
    helmets_info = GroupsInfo(
        element_id="Helmet", markers_pattern_re=r"Helmet_(\d+ - \d).*", label_sep="_"
    )
    df_plot = transform_df2plotly(
        input_df=features_filtered.copy(),
        groups_info=[helmets_info, darko_info, lo_info],
    )
    best_makers_df = filter_best_markers(
        elements_cat_df=df_plot.copy(), nan_counter_by_marker=best_markers_counter
    )
    figs = get_multi_element_trajectories(best_makers_df)
    for fig in figs:
        st.plotly_chart(fig, use_container_width=True)
