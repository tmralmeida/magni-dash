import os
import streamlit as st
from magni_dash.visualization.trajectories import show_file_traj_data
from magni_dash.config.constants import TRAJECTORY_SAMPLES_PATH


files = os.listdir(TRAJECTORY_SAMPLES_PATH)
files_target = list(filter(lambda x: x.endswith("pp.tsv"), files))


st.title("Magni Dashboard")
option = st.selectbox(
    label="File", options=files_target, key="input_file", label_visibility="visible"
)

if st.session_state.input_file:
    show_file_traj_data()
