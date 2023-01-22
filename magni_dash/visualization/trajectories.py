import matplotlib.pyplot as plt
import streamlit as st
import os
import re


from magni_dash.data_preprocessing.load import load_df
from magni_dash.data_preprocessing.trajectory_data import process_data
from magni_dash.config.constants import TRAJECTORY_SAMPLES_PATH


def show_file_traj_data():
    data_load_state = st.text("Loading data...")
    file_name = st.session_state["input_file"]
    raw_df = load_df(
        df_path=os.path.join(TRAJECTORY_SAMPLES_PATH, file_name),
        sep="\t",
        header=11,
        index_col="Frame",
    )
    processed_df = process_data(raw_df=raw_df)

    data_load_state.text("Loading data...done!")

    regex_pattern = re.compile(r"H\d+")
    helmet_number = regex_pattern.findall(file_name)[0][1:]
    st.write(
        processed_df[
            [f"Helmet_{helmet_number} - 1 X", f"Helmet_{helmet_number} - 1 Y"]
        ].head(5)
    )

    fig = plt.figure(figsize=(20, 10))
    plt.scatter(
        processed_df[f"Helmet_{helmet_number} - 1 X"],
        processed_df[f"Helmet_{helmet_number} - 1 Y"],
        s=1,
    )
    plt.title(f"Data from Helmet {helmet_number}", fontsize=40)
    plt.axis("off")
    st.pyplot(fig)
