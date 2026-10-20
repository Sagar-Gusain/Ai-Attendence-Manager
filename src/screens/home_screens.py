
import streamlit as st
from pathlib import Path
from src.components.header_home import header_home
from src.ui.base_layout import home_style, style_layout

def home_screen():
    style_layout()
    home_style()
    header_home()

    image_dir = Path(__file__).resolve().parents[1] / "components"

    teacher_img = image_dir / "Friendly Teacher with Checklist Board.png"
    student_img = image_dir / "Smiling Student with Open Book.png"

    # Define columns BEFORE using them
    left, teacher_col, student_col, right = st.columns(
        [1, 2, 2, 1],
        gap="large"
    )

    with teacher_col:
        with st.container(border=True):
            st.markdown(
                '<h3 class="portal-title">Teacher</h3>',
                unsafe_allow_html=True
            )

            st.image("src/components/Friendly Teacher with Checklist Board.png", width=250)

            if st.button(
                "Teacher Portal",
                key="teacher_btn",
                use_container_width=True
            ):
                st.session_state["login_state"] = "Teacher"
                st.rerun()

    with student_col:
        with st.container(border=True):
            st.markdown(
                '<h3 class="portal-title">Student</h3>',
                unsafe_allow_html=True
            )

            st.image("src/components/Smiling Student with Open Book.png", width=250)

            if st.button(
                "Student Portal",
                key="student_btn",
                use_container_width=True
            ):
                st.session_state["login_state"] = "Student"
                st.rerun()

    st.markdown(
        '<h2 class="home-subtitle">Attendance made Easy!</h2>',
        unsafe_allow_html=True
    )
