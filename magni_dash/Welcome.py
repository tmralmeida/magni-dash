import streamlit as st

st.set_page_config(page_title="Welcome")
st.write("# Welcome to Magni Dashboard! 👋")


st.markdown(
    """
   Magni is a data collection of human motion in 6 different scenarios. It includes
   160 minutes of motion on 4 acquisition days with a total of 30 unique
   participants. In addition to the static obstacles in the room,
   we augment the environment with semantic context, such
   as one-way passages and yellow tape markings for areas of caution.
"""
)