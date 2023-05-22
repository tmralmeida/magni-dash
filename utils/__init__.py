import streamlit as st


def clear_session_state():
    for key in st.session_state.keys():
        del st.session_state[key]
