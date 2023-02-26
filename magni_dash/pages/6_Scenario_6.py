import os
import streamlit as st
from magni_dash.visualization.trajectories import (
    load_data,
    play_single_trajectory,
    play_double_view_trajectories,
)
from magni_dash.config.constants import TRAJECTORY_SAMPLES_PATH

st.set_page_config(page_title="Scenario 6")
st.markdown("# Scenario 6")
st.sidebar.header("Scenario 6")
st.write(
    """Scenario 6 description"""
)


modes = [
    "raw data single view ",
    "raw data double view (2 plots)",
    "raw data double-view (overlayed)",
    "synched data single-view",
    "synched data double-view (2 plots)",
    "synched data double-view (overlayed)",
]
page = st.radio("Mode", modes)


files = os.listdir(TRAJECTORY_SAMPLES_PATH)
files_target = list(filter(lambda x: x.endswith("pp.tsv"), files))
if page == "raw data single view ":
    option = st.selectbox(
        label="File", options=files_target, key="input_file", label_visibility="visible"
    )
    if st.session_state.input_file:
        processed_df = load_data(input_file=st.session_state["input_file"])
        play_single_trajectory(
            input_file=st.session_state["input_file"],
            processed_df=processed_df,
        )
elif page == "raw data double view (2 plots)":
    splitted_file_name = list(map(lambda x: x.split("SC6"), files_target))
    scenarios6a_files = [
        sample for sample in splitted_file_name if list(sample[1])[0] == "A"
    ]
    scenarios6b_files = [
        sample for sample in splitted_file_name if list(sample[1])[0] == "B"
    ]
    options_per_scenario = {
        "SC6".join([file6a[0], file6a[1][1:]]): (
            "SC6".join(file6a),
            "SC6".join(file6b),
        )
        for file6a in scenarios6a_files
        for file6b in scenarios6b_files
        if list(file6a[1])[1:] == list(file6b[1])[1:] and file6a[0] == file6b[0]
    }
    options_drop_down = options_per_scenario.keys()
    option = st.selectbox(
        label="File",
        options=options_drop_down,
        label_visibility="visible",
        key="joint_file",
    )
    scenario6a_file, scenario6b_file = options_per_scenario[
        st.session_state["joint_file"]
    ]
    if st.session_state.joint_file:
        df_a, df_b = load_data(input_file=scenario6a_file), load_data(
            input_file=scenario6b_file
        )
        play_single_trajectory(input_file=scenario6a_file, processed_df=df_a)
        play_single_trajectory(input_file=scenario6b_file, processed_df=df_b)
elif page == "raw data double-view (overlayed)":
    splitted_file_name = list(map(lambda x: x.split("SC6"), files_target))
    scenarios6a_files = [
        sample for sample in splitted_file_name if list(sample[1])[0] == "A"
    ]
    scenarios6b_files = [
        sample for sample in splitted_file_name if list(sample[1])[0] == "B"
    ]
    options_per_scenario = {
        "SC6".join([file6a[0], file6a[1][1:]]): (
            "SC6".join(file6a),
            "SC6".join(file6b),
        )
        for file6a in scenarios6a_files
        for file6b in scenarios6b_files
        if list(file6a[1])[1:] == list(file6b[1])[1:] and file6a[0] == file6b[0]
    }
    options_drop_down = options_per_scenario.keys()
    option = st.selectbox(
        label="File",
        options=options_drop_down,
        label_visibility="visible",
        key="joint_file_overlayed",
    )
    scenario6a_file, scenario6b_file = options_per_scenario[
        st.session_state["joint_file_overlayed"]
    ]
    if st.session_state.joint_file_overlayed:
        df_a, df_b = load_data(input_file=scenario6a_file), load_data(
            input_file=scenario6b_file
        )
        input_files = dict(zip(["SC6A", "SC6B"], [scenario6a_file, scenario6b_file]))
        processed_dfs = dict(zip(["SC6A", "SC6B"], [df_a, df_b]))
        play_double_view_trajectories(
            input_files=input_files, processed_dfs=processed_dfs
        )

elif page == "synched data single-view":
    st.write("TODO")

elif page == "synched data double-view (2 plots)":
    st.write("TODO")

elif page == "synched data double-view (overlayed)":
    st.write("TODO")
