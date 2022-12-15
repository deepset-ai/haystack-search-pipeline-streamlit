import streamlit as st

def set_state_if_absent(key, value):
    if key not in st.session_state:
        st.session_state[key] = value

def set_initial_state():
    set_state_if_absent("question", "Ask something here?")
    set_state_if_absent("results", None)

def reset_results(*args):
    st.session_state.results = None