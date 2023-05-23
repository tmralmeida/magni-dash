import streamlit as st

st.set_page_config(page_title="Welcome", page_icon="👋")
st.write("# Welcome to Magni Dashboard!")


st.markdown(
    """
   THÖR-Magni is a data collection of human motion in 5 different scenarios. It includes
   ~3.5h of motion on 5 acquisition days with a total of 40 unique
   participants. In addition to the static obstacles in the room,
   we augment the environment with semantic context, such
   as one-way passages and yellow tape markings for areas of caution.
"""
)
