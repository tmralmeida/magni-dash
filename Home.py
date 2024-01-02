import streamlit as st
from PIL import Image

st.set_page_config(page_title="Home")
st.write("# THÖR-Magni Dashboard")


st.markdown(
    """
   THÖR-Magni is a data collection of human motion in 5 different scenarios. It includes
   ~3.5h of motion on 5 acquisition days with a total of 40 unique
   participants. In addition to the static obstacles in the room,
   we augment the environment with semantic context, such
   as one-way passages and yellow tape markings for areas of caution.
   You can check our publications at:
   * [IEEE RO-MAN '22 Workshop Proceedings: Towards Socially Intelligent Robots In Real World
   Applications (SIRRW 2022)](https://arxiv.org/abs/2208.14925)
   * [IEEE ICCV '23 Workshop Proceedings: Visual Perception for Navigation in Human Environments:
   The JackRabbot Human Motion Forecasting Dataset
   and Benchmark](https://ieeexplore.ieee.org/document/10350939)
   * [IEEE RO-MAN '23: Advantages of Multimodal versus Verbal-Only Robot-to-Human Communication
   with an Anthropomorphic Robotic Mock Driver](https://ieeexplore.ieee.org/abstract/document/10309629/?casa_token=V-OAu7v4-T0AAAAA:S_21Zd_uqZFQErXjZVjcurqfjm2zyrG8a29f5eFbLH2yDhJpVya4UVQKysIWN7P1_afNARDCKaw)
"""
)
layout_img = Image.open("images/logo.jpg")
st.image(layout_img, use_column_width=True)
