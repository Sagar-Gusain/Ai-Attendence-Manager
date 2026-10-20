
import streamlit as st
from pathlib import Path

def header_home():
    logo_path = Path(__file__).parent / "AttendX Graduation Checkmark Logo.png"

    _, center, _ = st.columns([1.7, 2, 1])

    with center:
        st.image(str(logo_path), width=140)

    st.markdown(
        '<h1 class="home-title">AttendX</h1>',
        unsafe_allow_html=True
    )
