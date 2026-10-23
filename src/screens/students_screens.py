import streamlit as st
from pathlib import Path
from src.database.db import check_student_exist, create_student, student_login
import streamlit as st

from PIL import Image
import numpy as np

def student_screen():

    # ===== PAGE STYLE =====
    st.markdown("""
    <style>
    .stApp {
        background: #E5E5FF;
    }

    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
    }

    .attendx-logo {
        font-size: 42px;
        font-weight: 900;
        color: #4F5FEA;
        letter-spacing: -2px;
        text-align: center;
        margin-bottom: 0;
    }

    .attendx-subtitle {
        text-align: center;
        color: #25263B;
        font-size: 29px;
        font-weight: 800;
        margin-top: 5px;
        margin-bottom: 28px;
    }

    .camera-label {
        font-size: 15px;
        font-weight: 700;
        color: #292A43;
        margin-bottom: 8px;
    }

    div.stButton > button {
        background: linear-gradient(90deg, #5965F2, #7257EB);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 12px 20px;
        font-size: 16px;
        font-weight: 700;
        min-height: 48px;
        transition: 0.2s;
    }

    div.stButton > button:hover {
        background: #414DD8;
        color: white;
        border: none;
        transform: translateY(-2px);
    }

    .footer-text {
        text-align: center;
        color: #555675;
        font-size: 13px;
        margin-top: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ===== HEADER =====
    left, middle, right = st.columns([1, 2, 1])

    with middle:
        st.markdown(
            '<div class="attendx-logo">✦ AttendX</div>',
            unsafe_allow_html=True
        )

    with right:
        if st.button("← Home", key="student_home"):
            st.session_state["login_state"] = None
            st.session_state["login_role"] = None
            st.rerun()

    st.markdown(
        '<div class="attendx-subtitle">'
        'Login Using Face Recognition</div>',
        unsafe_allow_html=True
    )

    # ===== CAMERA PANEL =====
    left, center, right = st.columns([0.7, 2.6, 0.7])

    with center:
        st.markdown(
            '<div class="camera-label">'
            '📸 Position your face in the center</div>',
            unsafe_allow_html=True
        )

        photo = st.camera_input(
            "Camera",
            key="student_face_camera",
            label_visibility="collapsed"
        )
        
        if photo:
            image= np.array(Image.open(photo))
        if st.button(
            "📸  Take Photo",
            key="student_take_photo",
            use_container_width=True
        ):
            if photo is None:
                st.warning("Please capture your face using the camera first.")
            else:
                st.success("Photo captured successfully!")

                # Connect face verification here.

    # ===== FOOTER =====
    st.markdown("""
        <div class="footer-text">
            Made with 💜 for smarter attendance · AttendX
        </div>
    """, unsafe_allow_html=True)