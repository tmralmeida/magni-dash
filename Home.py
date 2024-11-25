import streamlit as st
from PIL import Image

st.set_page_config(page_title="Home")
st.write("# THÖR-MAGNI Dashboard")

web, paper, tb, challenge = st.columns(4)
web.link_button(
    "Webpage", "http://thor.oru.se/magni.html", icon="🖥️"
)
paper.link_button(
    "Paper", "https://journals.sagepub.com/doi/10.1177/02783649241274794", icon="📄"
)
tb.link_button(
    "Toolbox", "https://github.com/tmralmeida/thor-magni-tools", icon="🔧"
)
challenge.link_button(
    "Challenge",
    "https://github.com/tmralmeida/lhmp-thor-magni-challenge-extras",
    icon="🔥",
)


st.markdown(
    """
    We present a new large dataset of indoor human and robot navigation and interaction, called
    THÖR-MAGNI, that is designed to facilitate research on social human navigation: for example,
    modeling and predicting human motion, analyzing goal-oriented interactions between humans and
    robots, and investigating visual attention in a social interaction context. THÖR-MAGNI was
    created to fill a gap in available datasets for human motion analysis and HRI. This gap is
    characterized by a lack of comprehensive inclusion of exogenous factors and essential target
    agent cues, which hinders the development of robust models capable of capturing the relationship
    between contextual cues and human behavior in different scenarios. Unlike existing datasets,
    THÖR-MAGNI includes a broader set of contextual features and offers multiple scenario variations
    to facilitate factor isolation. The dataset includes many social human-human and human-robot
    interaction scenarios, rich context annotations, and multi-modal data, such as walking
    trajectories, gaze-tracking data, and lidar and camera streams recorded from a mobile robot.
   You can check our publications using the dataset:
   * [IEEE Robotics and Automation Letters (RA-L) '24: Trajectory Prediction for Heterogeneous
   Agents: A Performance Analysis on Small and
   Imbalanced Datasets](https://ieeexplore.ieee.org/abstract/document/10545544)
   * [IEEE RO-MAN '24: "Human Gaze and Head Rotation during Navigation, Exploration and Object
   Manipulation in Shared Environments with Robots"](https://arxiv.org/abs/2406.06300)
   * [IEEE RO-MAN '23: "Advantages of Multimodal versus Verbal-Only Robot-to-Human Communication
   with an Anthropomorphic Robotic Mock Driver"](https://ieeexplore.ieee.org/abstract/document/10309629/?casa_token=V-OAu7v4-T0AAAAA:S_21Zd_uqZFQErXjZVjcurqfjm2zyrG8a29f5eFbLH2yDhJpVya4UVQKysIWN7P1_afNARDCKaw)
   * [IEEE ICCV '23 Workshop Proceedings: Visual Perception for Navigation in Human Environments:
   The JackRabbot Human Motion Forecasting Dataset
   and Benchmark](https://ieeexplore.ieee.org/document/10350939)
"""
)
layout_img = Image.open("images/logo.jpg")
st.image(layout_img, use_container_width=True)
