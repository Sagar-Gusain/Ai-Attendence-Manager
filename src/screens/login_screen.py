import streamlit as st

def login_screen():
    st.header("Login")
    role = st.selectbox("Select Role", ["Student", "Teacher"])
    if st.button("Login"):
        st.session_state["login_state"] = role
        st.rerun()
