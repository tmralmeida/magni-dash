import plotly.express as px
import streamlit as st
import os
import re


from magni_dash.data_preprocessing.load import load_df
from magni_dash.data_preprocessing.trajectory_data import process_data
from magni_dash.config.constants import TRAJECTORY_SAMPLES_PATH


def load_data():
    raw_df = load_df(
        df_path=os.path.join(TRAJECTORY_SAMPLES_PATH, st.session_state["input_file"]),
        sep="\t",
        header=11,
        index_col="Frame",
    )
    processed_df = process_data(raw_df=raw_df)
    st.session_state["df"] = processed_df


def play_data():
    processed_df = st.session_state["df"]
    regex_pattern = re.compile(r"H\d+")
    helmet_number = regex_pattern.findall(st.session_state["input_file"])[0][1:]
    fig = px.line(
        processed_df[: st.session_state["current_frame"]],
        x=f"Helmet_{helmet_number} - 1 X",
        y=f"Helmet_{helmet_number} - 1 Y",
        title=f"Data from Helmet {helmet_number}",
    )
    fig.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        xaxis_range=[
            processed_df[f"Helmet_{helmet_number} - 1 X"].min(),
            processed_df[f"Helmet_{helmet_number} - 1 X"].max(),
        ],
        yaxis_range=[
            processed_df[f"Helmet_{helmet_number} - 1 Y"].min(),
            processed_df[f"Helmet_{helmet_number} - 1 Y"].max(),
        ],
    )
    st.plotly_chart(fig, use_container_width=True)
