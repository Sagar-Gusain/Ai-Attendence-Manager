
import streamlit as st
from pathlib import Path

from src.ui.base_layout import teacher_style
from src.database.db import check_teacher_exist, create_teacher, teacher_login


def teacher_screen():
    # If teacher is already logged in, show the teacher dashboard
    if st.session_state.get("teacher_user"):
        teacher_dashboard(st.session_state["teacher_user"])
        return

    teacher_style()

    # ===== CUSTOM STYLING =====
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(
                135deg, #FFF1F5 0%, #FCE7F3 55%, #FBCFE8 100%
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

        /* Logo and brand */
        .brand-title {
            color: #831843 !important;
            font-size: 1.8rem !important;
            font-weight: 800 !important;
            margin: 0 !important;
        }

        .brand-subtitle {
            color: #9D174D !important;
            font-size: 0.95rem;
            margin-top: 8px;
            line-height: 1.5;
        }

        /* Dashboard heading */
        .portal-title {
            text-align: center;
            color: #831843 !important;
            font-size: 2.5rem !important;
            font-weight: 800 !important;
            margin: 20px 0 25px 0 !important;
        }

        /* Login card */
        .login-card {
            background: rgba(255, 255, 255, 0.95);
            border: 1px solid #F9A8D4;
            border-radius: 22px;
            padding: 24px;
            box-shadow: 0 12px 32px rgba(131, 24, 67, 0.12);
            text-align: center;
            margin-bottom: 12px;
        }

        .login-card h2 {
            color: #831843 !important;
            font-size: 1.8rem !important;
            margin: 12px 0 18px 0 !important;
        }

        .login-card p {
            color: #9D174D !important;
        }

        .portal-badge {
            color: #BE185D !important;
            font-weight: 800;
            letter-spacing: 2px;
            font-size: 0.8rem;
        }

        /* Inputs */
        .stTextInput label {
            color: #831843 !important;
            font-weight: 600 !important;
        }

        .stTextInput input {
            background: #FFFFFF !important;
            color: #4A1942 !important;
            border: 1px solid #F9A8D4 !important;
            border-radius: 10px !important;
        }

        .stCheckbox label {
            color: #831843 !important;
        }

        /* Buttons */
        .stFormSubmitButton > button {
            width: 100%;
            border-radius: 12px !important;
            min-height: 46px;
            font-weight: 700 !important;
            transition: all 0.2s ease;
        }

        /* Sign Up Button (Primary Gradient) */
        .st-key-teacher_signup_btn button {
            background: linear-gradient(
                135deg, #DB2777, #BE185D
            ) !important;
            color: #FFFFFF !important;
            border: none !important;
            box-shadow: 0 4px 12px rgba(190, 24, 93, 0.25);
        }

        .st-key-teacher_signup_btn button:hover {
            background: #9D174D !important;
            box-shadow: 0 6px 16px rgba(190, 24, 93, 0.35);
            transform: translateY(-1px);
        }

        .st-key-teacher_signup_btn button p {
            color: #FFFFFF !important;
            font-weight: 700 !important;
        }

        /* Log In Button (Secondary Outline) */
        .st-key-teacher_login_btn button {
            background: #FFFFFF !important;
            color: #BE185D !important;
            border: 2px solid #DB2777 !important;
            box-shadow: 0 4px 12px rgba(190, 24, 93, 0.08);
        }

        .st-key-teacher_login_btn button:hover {
            background: #FDF2F8 !important;
            border-color: #9D174D !important;
            transform: translateY(-1px);
        }

        .st-key-teacher_login_btn button p {
            color: #BE185D !important;
            font-weight: 700 !important;
        }

        .st-key-teacher_login_btn button:hover p {
            color: #9D174D !important;
        }

        /* External Redirect Button */
        .st-key-teacher_to_login_screen_btn button {
            width: 100%;
            background: #FFFFFF !important;
            color: #BE185D !important;
            border: 2px solid #DB2777 !important;
            border-radius: 12px !important;
            min-height: 44px;
            font-weight: 700 !important;
            box-shadow: 0 4px 12px rgba(190, 24, 93, 0.08);
            transition: all 0.2s ease;
        }

        .st-key-teacher_to_login_screen_btn button:hover {
            background: #FDF2F8 !important;
            border-color: #9D174D !important;
            transform: translateY(-1px);
        }

        .st-key-teacher_to_login_screen_btn button p {
            color: #BE185D !important;
            font-weight: 700 !important;
        }

        .st-key-teacher_to_login_screen_btn button:hover p {
            color: #9D174D !important;
        }

        /* Back button */
        .stButton > button {
            border-radius: 10px !important;
            font-weight: 600 !important;
        }

        .login-footer {
            text-align: center;
            color: #9D174D;
            font-size: 0.85rem;
            margin-top: 18px;
        }
    </style>
    """, unsafe_allow_html=True)

    # ===== BACK TO HOME =====
    if st.button(
        "← Back to Home",
        key="teacher_back_home",
        shortcut="ctrl+h"
    ):
        st.session_state["login_state"] = None
        st.rerun()
   
    # ===== DASHBOARD TITLE =====
    st.markdown("""
        <h1 class="portal-title">Teacher Registration</h1>
    """, unsafe_allow_html=True)

    # ===== SIGN UP FORM =====
    left, center, right = st.columns([1, 1.15, 1])

    with center:
        st.markdown("""
            <div class="login-card">
                <div class="portal-badge">TEACHER PORTAL</div>
                <h2>Create Account</h2>
                <p>Register to manage classroom attendance and records.</p>
            </div>
        """, unsafe_allow_html=True)

        with st.form("teacher_id"):
            name = st.text_input(
                " ID",
                placeholder="e.g. 123",
                key="teacher_signup_id"
            )

            email = st.text_input(
                "Teacher Name",
                placeholder="e.g. Dr. Jane Smith",
                key="teacher_signup_name"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Create a strong password",
                key="teacher_signup_password"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Confirm your password",
                key="teacher_signup_confirm_password"
            )


            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                signup_submitted = st.form_submit_button(
                    "Sign Up →",
                    key="teacher_signup_btn",
                    use_container_width=True
                )

            with btn_col2:
                login_submitted = st.form_submit_button(
                    "Log In",
                    key="teacher_login_btn",
                    use_container_width=True
                )

            # Log In button → take user to the login screen
            if login_submitted:
                st.session_state["login_state"] = "Login"
                st.session_state["login_role"] = "Teacher"
                st.rerun()



            # Handle Sign Up submission
            if signup_submitted:
                teacher_id = name.strip()
                teacher_name = email.strip()

                if not teacher_id:
                    st.warning("Please enter your Teacher ID.")
                elif not teacher_name:
                    st.warning("Please enter your full name.")
                elif not password:
                    st.warning("Please enter a password.")
                elif len(password) < 6:
                    st.warning("Password must be at least 6 characters long.")
                elif password != confirm_password:
                    st.error("Passwords do not match. Please try again.")
                else:
                    try:
                        if not check_teacher_exist(teacher_id):
                            st.error("This Teacher ID is already registered.")
                        else:
                            result = create_teacher(
                                teacher_id,
                                teacher_name,
                                password
                            )

                            if result and result.data:
                                st.success(
                                    f"🎉 Account created successfully for {teacher_name}!"
                                )
                                st.info("You can now click 'Log In' to access your account.")
                            else:
                                st.error("Failed to create account. Please try again.")

                    except Exception as e:
                        st.error(f"Database error: {str(e)}")
        st.markdown("""
            <div style="text-align: center; margin-top: 16px; margin-bottom: 8px;">
                <span style="color: #9D174D; font-size: 0.9rem; font-weight: 500;">
                    Already have an account?
                </span>
            </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Already have an account? Log In →",
            key="teacher_to_login_screen_btn",
            use_container_width=True
        ):
            st.session_state["login_state"] = "Login"
            st.session_state["login_role"] = "Teacher"
            st.rerun()

        st.markdown("""
            <p class="login-footer">
                Secure access · AttendX Attendance Management
            </p>
        """, unsafe_allow_html=True)




def teacher_dashboard(user=None):
    teacher_style()

    if user is None:
        user = st.session_state.get("teacher_user", {
            "name": "Teacher",
            "user_name": "teacher@college.edu",
            "teacher_id": 1
        })

    teacher_name = user.get("name", "Teacher")

    col1, col2 = st.columns([5, 1])
    with col2:
        if st.button("Log Out 🚪", key="dash_logout_btn"):
            st.session_state.pop("teacher_user", None)
            st.session_state["login_state"] = None
            st.rerun()

    st.markdown(f"""
        <div style="
            background: rgba(255, 255, 255, 0.95);
            border: 1px solid #F9A8D4;
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(131, 24, 67, 0.08);
            margin-top: 20px;
        ">
            <h1 style="color: #831843; font-size: 2.5rem; font-weight: 800; margin-bottom: 10px;">
                Welcome, {teacher_name}! 👋
            </h1>
        </div>
    """, unsafe_allow_html=True)


# Alias supporting exact user spelling
teacher_dashbord = teacher_dashboard


