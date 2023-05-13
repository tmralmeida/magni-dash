import streamlit as st
import pandas as pd


st.markdown("# LET'S DOOO IT!!!! 💪")

info = {
    "DONE 🙌": [
        "Aligning gaze + trajectories",
        "80% of trajectories post processed",
        "75% of videos blurred faces",
        "code for Lidar visualization",
        "Demo dashboard",
    ],
    "MISSING 😢": [
        "Align EDA",
        "Discuss CSV format",
        "Resolve Ethical Approval (Scenario 6)",
        "20% of trajectories post processing",
        "25% of videos",
        "Website for dashboard",
        "Calibration EYTs (intrinsics)",
        "Offset helmets & glasses",
        "Lidar bagfiles",
        "Paper writing",
    ],
    "WHO 🙋": [
        "",
        "Tiago,",
        "Everyone + Erika",
        "students, Tiago",
        "",
        "Martin + Tiago (discussion)",
        "Tim",
        "Tim",
        "Yufei",
        "Tim, Tiago",
    ],
}

max_nfields = max([len(v) for v in info.values()])
info = {k: v + [""] * (max_nfields - len(v)) for k, v in info.items()}

df = pd.DataFrame.from_dict(info)
st.table(df)
