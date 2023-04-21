import streamlit as st


def run_configs(scenario_id: int):
    st.set_page_config(page_title=f"Scenario {scenario_id}", layout="wide")
    st.markdown(f"# Scenario {scenario_id}")
    st.sidebar.header(f"Scenario {scenario_id}")
    st.write(f"""Scenario {scenario_id} description""")
