import streamlit as st
from pathlib import Path
from src.database.db import teacher_login


def login_screen():
    # ===== CUSTOM STYLING =====
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(
                135deg, #F0F4FF 0%, #E0E7FE 50%, #D8B4FE 100%
            ) !important;
        }

        [data-testid="stMain"] {
            background: transparent !important;
        }

        .block-container {
            max-width: 1100px !important;
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
        }

        /* Portal heading */
        .login-page-title {
            text-align: center;
            color: #1E1B4B !important;
            font-size: 2.4rem !important;
            font-weight: 800 !important;
            margin: 15px 0 25px 0 !important;
        }

        /* Login card */
        .login-card {
            background: rgba(255, 255, 255, 0.95);
            border: 1px solid #C7D2FE;
            border-radius: 22px;
            padding: 24px;
            box-shadow: 0 12px 32px rgba(30, 27, 75, 0.12);
            text-align: center;
            margin-bottom: 12px;
        }

        .login-card h2 {
            color: #1E1B4B !important;
            font-size: 1.8rem !important;
            margin: 10px 0 12px 0 !important;
        }

        .login-card p {
            color: #4338CA !important;
            font-size: 0.95rem;
            margin: 0;
        }

        .portal-badge {
            color: #4F46E5 !important;
            font-weight: 800;
            letter-spacing: 2px;
            font-size: 0.8rem;
        }

        /* Inputs */
        .stTextInput label, .stSelectbox label {
            color: #1E1B4B !important;
            font-weight: 600 !important;
        }

        .stTextInput input {
            background: #FFFFFF !important;
            color: #1E1B4B !important;
            border: 1px solid #C7D2FE !important;
            border-radius: 10px !important;
        }

        .stCheckbox label {
            color: #1E1B4B !important;
        }

        /* Submit Button */
        .st-key-login_submit_btn button {
            width: 100%;
            background: linear-gradient(
                135deg, #4F46E5, #4338CA
            ) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 12px !important;
            min-height: 46px;
            font-weight: 700 !important;
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25);
            transition: all 0.2s ease;
        }

        .st-key-login_submit_btn button:hover {
            background: #3730A3 !important;
            box-shadow: 0 6px 16px rgba(79, 70, 229, 0.35);
            transform: translateY(-1px);
        }

        .st-key-login_submit_btn button p {
            color: #FFFFFF !important;
            font-weight: 700 !important;
        }

        /* Switch to Sign Up Buttons */
        .st-key-login_to_student_signup_btn button,
        .st-key-login_to_teacher_signup_btn button {
            width: 100%;
            background: #FFFFFF !important;
            color: #4F46E5 !important;
            border: 2px solid #4F46E5 !important;
            border-radius: 12px !important;
            min-height: 44px;
            font-weight: 700 !important;
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.08);
            transition: all 0.2s ease;
        }

        .st-key-login_to_student_signup_btn button:hover,
        .st-key-login_to_teacher_signup_btn button:hover {
            background: #EEF2FF !important;
            border-color: #3730A3 !important;
            transform: translateY(-1px);
        }

        .st-key-login_to_student_signup_btn button p,
        .st-key-login_to_teacher_signup_btn button p {
            color: #4F46E5 !important;
            font-weight: 700 !important;
        }

        .st-key-login_to_student_signup_btn button:hover p,
        .st-key-login_to_teacher_signup_btn button:hover p {
            color: #3730A3 !important;
        }

        /* Back button */
        .stButton > button {
            border-radius: 10px !important;
            font-weight: 600 !important;
        }

        .login-footer {
            text-align: center;
            color: #4338CA;
            font-size: 0.85rem;
            margin-top: 18px;
        }
    </style>
    """, unsafe_allow_html=True)

    # ===== BACK TO HOME =====
    if st.button(
        "← Back to Home",
        key="login_back_home",
        shortcut="ctrl+h"
    ):
        st.session_state["login_state"] = None
        st.rerun()

    # ===== DASHBOARD TITLE =====
    st.markdown("""
        <h1 class="login-page-title">AttendX Portal Login</h1>
    """, unsafe_allow_html=True)

    # ===== LOGIN FORM =====
    left, center, right = st.columns([1, 1.1, 1])

    with center:
        st.markdown("""
            <div class="login-card">
                <div class="portal-badge">SECURE ACCESS</div>
                <h2>Welcome Back!</h2>
                <p>Sign in to your AttendX account</p>
            </div>
        """, unsafe_allow_html=True)

        current_role = st.session_state.get("login_role", "Teacher")
        roles = ["Teacher"]
        default_index = roles.index(current_role) if current_role in roles else 0

        with st.form("main_login_form"):
            selected_role = st.selectbox(
                "Select Role",
                options=roles,
                index=default_index,
                key="login_selected_role"
            )

            email = st.text_input(
                "Email address",
                placeholder="you@college.edu",
                key="login_email"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="login_password"
            )

            remember = st.checkbox("Remember me", key="login_remember")

            login_submitted = st.form_submit_button(
                "Sign In →",
                key="login_submit_btn",
                use_container_width=True
            )

            if login_submitted:
                cleaned_email = email.strip()
                if not cleaned_email or not password:
                    st.warning("Please enter your email and password.")
                elif selected_role == "Teacher":
                    user = teacher_login(cleaned_email, password)
                    if user:
                        st.session_state["teacher_user"] = user
                        st.session_state["login_role"] = "Teacher"
                        st.session_state["login_state"] = "Dashboard"
                        st.rerun()
                    else:
                        st.error("Invalid email or password. Please try again.")


                else:
                    st.info("Student authentication backend will be connected soon.")

        st.markdown("""
            <div style="text-align: center; margin-top: 18px; margin-bottom: 8px;">
                <span style="color: #4338CA; font-size: 0.9rem; font-weight: 500;">
                    Don't have an account?
                </span>
            </div>
        """, unsafe_allow_html=True)

        sign_col1, sign_col2 = st.columns(2)
        with sign_col1:
            if st.button(
                "Sign Up as Student →",
                key="login_to_student_signup_btn",
                use_container_width=True
            ):
                st.session_state["login_state"] = "Student"
                st.session_state["login_role"] = "Student"
                st.rerun()

        with sign_col2:
            if st.button(
                "Sign Up as Teacher →",
                key="login_to_teacher_signup_btn",
                use_container_width=True
            ):
                st.session_state["login_state"] = "Teacher"
                st.session_state["login_role"] = "Teacher"
                st.rerun()

        st.markdown("""
            <p class="login-footer">
                Secure access · AttendX Attendance Management
            </p>
        """, unsafe_allow_html=True)
