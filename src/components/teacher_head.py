
import streamlit as st
from pathlib import Path


def teacher_head():
    logo_path = (
        Path(__file__).parent
        / "AttendX Graduation Checkmark Logo.png"
    )

    # Logo and text together in one row
    left, logo_col, text_col, right = st.columns([1, 0.7, 1.5, 1])

    with logo_col:
        if logo_path.exists():
            st.image(str(logo_path), width=100)

    with text_col:
        st.markdown("""
            <div style="
                padding-top: 15px;
                text-align: left;
            ">
                <h2 style="
                    color: #831843;
                    font-size: 1.8rem;
                    font-weight: 800;
                    margin: 0;
                ">AttendX</h2>
                <p style="
                    color: #9D174D;
                    font-size: 0.95rem;
                    line-height: 1.5;
                    margin-top: 8px;
                ">
                    Smart Attendance<br>
                    Management System
                </p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <h1 style="
            text-align: center;
            color: #831843;
            font-size: 2.3rem;
            font-weight: 800;
            margin-top: 20px;
            margin-bottom: 25px;
        ">Teacher Screen</h1>
    """, unsafe_allow_html=True)
