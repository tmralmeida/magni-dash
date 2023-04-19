import os
import re
import streamlit as st
from collections import namedtuple
from magni_dash.st_components.cache import load_df, process_data, extract_features
from magni_dash.st_components.scenario6 import *
from magni_dash.utils.scenario6 import get_files_name_mapping
from magni_dash.visualization.trajectories import (
    get_single_trajectory,
    get_double_overlayed_view,
)


from magni_dash.config.constants import TRAJECTORY_SAMPLES_PATH


def run_preprocess_trajectory(input_file_name: str) -> None:
    raw_df = load_df(
        df_path=os.path.join(TRAJECTORY_SAMPLES_PATH, input_file_name),
        sep="\t",
        header=11,
        index_col="Frame",
    )
    processed_df = process_data(raw_df=raw_df)
    return processed_df


run_configs()

modes = [
    "Single file",
    "6A vs 6B",
    "Synched single file",
    "synched 6A vs 6B",
]
page = st.sidebar.radio("Mode", modes)
files = os.listdir(TRAJECTORY_SAMPLES_PATH)
files_target = list(filter(lambda x: x.endswith("pp.tsv"), files))
DoubleViewInputs = namedtuple(
    "DoubleViewInputs", ["input_file", "trajectory_df", "features_df"]
)
re_pattern_helmet_number = re.compile(r"H\d+")
if page == "Single file":
    input_file = st.sidebar.selectbox(
        label="File", options=files_target, key="input_file", label_visibility="visible"
    )
    helmet_number = re_pattern_helmet_number.findall(input_file)[0][1:]
    if st.session_state.input_file:
        preprocessed_df = run_preprocess_trajectory(input_file)
        n_markers = int(
            preprocessed_df[
                preprocessed_df.columns[
                    (preprocessed_df.columns.str.startswith("Helmet"))
                ]
            ].shape[1]
            / 2
        )
        marker = st.sidebar.radio("Marker to visualize", range(1, n_markers + 1))

        features_df = extract_features(preprocessed_df, helmet_number=helmet_number)
        figs = get_single_trajectory(
            helmet_number=helmet_number,
            marker=marker,
            input_file=input_file,
            processed_df=preprocessed_df,
            tab_component=st,
            features_df=features_df,
        )
        for fig in figs:
            st.plotly_chart(fig, use_container_width=True)

elif page == "6A vs 6B":
    options_per_scenario = get_files_name_mapping(files_target)
    input_file = st.sidebar.selectbox(
        label="File",
        options=options_per_scenario.keys(),
        label_visibility="visible",
        key="joint_file",
    )
    helmet_number = re_pattern_helmet_number.findall(input_file)[0][1:]
    scenario6a_file, scenario6b_file = options_per_scenario[
        st.session_state["joint_file"]
    ]
    if st.session_state.joint_file:
        df_a, df_b = run_preprocess_trajectory(
            input_file_name=scenario6a_file
        ), run_preprocess_trajectory(input_file_name=scenario6b_file)
        n_markers = int(
            df_a[df_a.columns[(df_a.columns.str.startswith("Helmet"))]].shape[1] / 2
        )
        marker = st.sidebar.radio("Marker to visualize", range(1, n_markers + 1))
        features_df_a = extract_features(df_a, helmet_number=helmet_number)
        features_df_b = extract_features(df_b, helmet_number=helmet_number)
        inputs_specfications = dict(
            SC6A=DoubleViewInputs(scenario6a_file, df_a, features_df_a),
            SC6B=DoubleViewInputs(scenario6b_file, df_b, features_df_b),
        )
        figs = get_double_overlayed_view(inputs_specfications, marker=marker)
        for fig in figs:
            st.plotly_chart(fig, use_container_width=True)

elif page == "Synched single file":
    st.write("TODO")

elif page == "synched 6A vs 6B":
    st.write("TODO")
