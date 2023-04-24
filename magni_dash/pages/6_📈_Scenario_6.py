import os
import re
import streamlit as st
from functools import partial
from collections import namedtuple
from magni_dash.st_components.cache import load_df, extract_features, preprocess_df
from magni_dash.st_components.common import run_configs
from magni_dash.utils.scenario6 import get_files_name_mapping
from magni_dash.visualization.single_trajectory import (
    get_single_trajectory,
    get_double_overlayed_view,
)
from magni_dash.config.constants import TRAJECTORY_SAMPLES_PATH


SCENARIO6_PATH = os.path.join(TRAJECTORY_SAMPLES_PATH, "Scenario6")


run_configs(scenario_id=6)

modes = [
    "Single file",
    "6A vs 6B",
    "Synched single file",
    "synched 6A vs 6B",
]
page = st.sidebar.radio("Mode", modes)
files = os.listdir(SCENARIO6_PATH)
files_target = list(filter(lambda x: x.endswith("pp.tsv"), files))
DoubleViewInputs = namedtuple(
    "DoubleViewInputs", ["helmet_label", "trajectory_df", "features_df"]
)
re_pattern_helmet_number = re.compile(r"H\d+")
load_data = partial(load_df, header=11, sep="\t", index_col="Frame")
extract_features_sc6 = partial(extract_features, darko_label="DARKO_Robot")
if page == "Single file":
    input_file = st.sidebar.selectbox(
        label="File", options=files_target, key="input_file", label_visibility="visible"
    )
    helmet_label = "Helmet_" + re_pattern_helmet_number.findall(input_file)[0][1:]
    if st.session_state.input_file:
        df_path = os.path.join(SCENARIO6_PATH, input_file)
        raw_df = load_data(
            df_path=df_path,
        )
        preprocessed_df = preprocess_df(raw_df.copy())
        n_markers = int(
            preprocessed_df[
                preprocessed_df.columns[
                    (preprocessed_df.columns.str.startswith("Helmet"))
                ]
            ].shape[1]
            / 2
        )
        marker = st.sidebar.radio("Marker to visualize", range(1, n_markers + 1))

        features_df = extract_features_sc6(
            preprocessed_df.copy(), magents_labels=helmet_label
        )
        figs = get_single_trajectory(
            helmet_label=helmet_label,
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
    helmet_label = "Helmet_" + re_pattern_helmet_number.findall(input_file)[0][1:]
    scenario6a_file, scenario6b_file = options_per_scenario[
        st.session_state["joint_file"]
    ]
    if st.session_state.joint_file:
        df_a = load_data(df_path=os.path.join(SCENARIO6_PATH, scenario6a_file))
        df_b = load_data(df_path=os.path.join(SCENARIO6_PATH, scenario6b_file))
        n_markers = int(
            df_a[df_a.columns[(df_a.columns.str.startswith("Helmet"))]].shape[1] / 2
        )
        marker = st.sidebar.radio("Marker to visualize", range(1, n_markers + 1))
        features_df_a = extract_features_sc6(df_a.copy(), magents_labels=helmet_label)
        features_df_b = extract_features_sc6(df_b.copy(), magents_labels=helmet_label)
        inputs_specfications = dict(
            SC6A=DoubleViewInputs(helmet_label, df_a, features_df_a),
            SC6B=DoubleViewInputs(helmet_label, df_b, features_df_b),
        )
        figs = get_double_overlayed_view(inputs_specfications, marker=marker)
        for fig in figs:
            st.plotly_chart(fig, use_container_width=True)

elif page == "Synched single file":
    st.write("TODO")

elif page == "synched 6A vs 6B":
    st.write("TODO")
