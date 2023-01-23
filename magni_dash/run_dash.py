import os
import streamlit as st
from magni_dash.visualization.trajectories import load_data, play_data
from magni_dash.config.constants import TRAJECTORY_SAMPLES_PATH


st.title("Magni Dashboard")
modes = ["raw data", "synchronized data"]
page = st.radio("Mode", modes)

if page == "raw data":
    files = os.listdir(TRAJECTORY_SAMPLES_PATH)
    files_target = list(filter(lambda x: x.endswith("pp.tsv"), files))
    option = st.selectbox(
        label="File", options=files_target, key="input_file", label_visibility="visible"
    )
    if st.session_state.input_file:
        load_data()
        min_frame, max_frame = int(st.session_state["df"].index.min()), int(
            st.session_state["df"].index.max()
        )
        frame = st.slider(
            label="Frame",
            min_value=min_frame,
            max_value=max_frame,
            value=min_frame,
            step=1,
            key="current_frame",
        )
        play_data()
elif page == "synchronized data":
    st.write("TODO")
