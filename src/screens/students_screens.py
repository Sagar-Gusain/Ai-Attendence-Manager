import streamlit as st
from PIL import Image
import numpy as np
from src.database.db import check_student_exist, create_student, student_login
from src.pipeline.face_pipeline import predict_attendance, process_image

def student_dashboard(user=None):
    if user is None:
        user = st.session_state.get("student_user", {})

    student_name = user.get("name") or st.session_state.get("name", "Student")
    student_id = user.get("student_id") or st.session_state.get("login_id", "N/A")

    # Styling for student dashboard
    st.markdown("""
    <style>
    .stApp {
        background: #E5E5FF;
    }
    .student-card {
        background: rgba(255, 255, 255, 0.95);
        border: 1px solid #C7D2FE;
        border-radius: 20px;
        padding: 35px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(79, 95, 234, 0.12);
        margin-top: 15px;
        margin-bottom: 25px;
    }
    .student-badge {
        display: inline-block;
        background: #DCFCE7;
        color: #166534;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 14px;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([5, 1])
    with col2:
        if st.button("Log Out 🚪", key="student_logout_btn"):
            st.session_state.pop("student_user", None)
            st.session_state.pop("name", None)
            st.session_state.pop("login_id", None)
            st.session_state.pop("attendance_success_msg", None)
            st.session_state["login_state"] = None
            st.rerun()

    st.markdown(f"""
        <div class="student-card">
            <h1 style="color: #4F5FEA; font-size: 2.4rem; font-weight: 800; margin-bottom: 5px;">
                Welcome, {student_name}! 🎓
            </h1>
            <p style="color: #555675; font-size: 1.1rem; margin-bottom: 12px;">
                Student ID: <strong>{student_id}</strong>
            </p>
            <div class="student-badge">
                ✅ Attendance Verified & Recorded for Today
            </div>
        </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.markdown("### 📋 Student Profile")
            st.write(f"**Name:** {student_name}")
            st.write(f"**Student ID:** {student_id}")
            st.write("**Biometrics Status:** Registered & Active")
    with c2:
        with st.container(border=True):
            st.markdown("### ⚙️ Quick Actions")
            if st.button("📸 Mark Attendance Again", key="re_mark_btn", use_container_width=True):
                st.session_state.pop("student_user", None)
                st.session_state["login_state"] = "Student"
                st.rerun()


# Alias supporting alternate spelling
student_dashbord = student_dashboard


def student_screen():
    # If student is already logged in, route directly to the dashboard
    if st.session_state.get("student_user"):
        student_dashboard(st.session_state["student_user"])
        return
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
        font-size: 24px;
        font-weight: 800;
        margin-top: 5px;
        margin-bottom: 25px;
    }

    .camera-label {
        font-size: 16px;
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
        margin-top: 40px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ===== HEADER =====
    st.markdown('<h1 class="attendx-logo">AttendX</h1>', unsafe_allow_html=True)
    st.markdown('<p class="attendx-subtitle">Student Facial Attendance Portal</p>', unsafe_allow_html=True)

    top_col1, top_col2, top_col3 = st.columns([1, 2, 1])
    with top_col1:
        if st.button("⬅️ Home", key="student_back_home"):
            st.session_state["login_state"] = None
            st.session_state.pop("face_unknown", None)
            st.session_state.pop("student_face_image", None)
            st.session_state.pop("login_id", None)
            st.rerun()

    # Feedback messages from previous action
    if st.session_state.get("reg_success_msg"):
        st.success(st.session_state.pop("reg_success_msg"))

    if st.session_state.get("attendance_success_msg"):
        st.success(st.session_state.pop("attendance_success_msg"))

    # ===== CAMERA PANEL =====
    left, center, right = st.columns([0.7, 2.6, 0.7])

    with center:
        st.markdown(
            '<div class="camera-label">'
            '📸 Position your face in the center and click "Take Photo" below</div>',
            unsafe_allow_html=True
        )

        # Camera widget
        photo = st.camera_input(
            "Camera",
            key="student_face_camera",
            label_visibility="collapsed"
        )

        if photo is not None:
            image = np.array(Image.open(photo).convert("RGB"))
            st.session_state["student_face_image"] = image

        if st.button(
            "📸 Take Photo & Verify",
            key="student_take_photo",
            use_container_width=True
        ):
            image = st.session_state.get("student_face_image")

            if image is None:
                st.warning("Please capture your face using the camera above first.")
            else:
                with st.spinner("Recognizing face..."):
                    detector_id = predict_attendance(image)

                if detector_id is not None and detector_id != "unknown":
                    student_info = student_login(detector_id)
                    student_name = student_info.get("name", f"Student {detector_id}") if student_info else f"Student {detector_id}"
                    
                    st.session_state["face_unknown"] = False
                    st.session_state["student_user"] = student_info or {"student_id": detector_id, "name": student_name}
                    st.session_state["name"] = student_name
                    st.session_state["login_id"] = detector_id
                    st.session_state["login_state"] = "Student_Dashboard"
                    st.rerun()

                else:
                    st.session_state["face_unknown"] = True
                    st.session_state["face_recognition_failed"] = True
                    st.rerun()

        # Render the registration form if face is not recognized
        if st.session_state.get("face_unknown", False):
            st.markdown("---")
            if st.session_state.get("face_recognition_failed"):
                st.warning("⚠️ Face not recognized or not registered yet. Please enter your details below to register your face.")

            st.markdown("### 📝 Register your face")

            student_name = st.text_input(
                "Student Name",
                key="new_student_name"
            )

            student_id = st.text_input(
                "Student ID (Numeric)",
                key="new_student_id"
            )

            if st.button("Register Face", key="register_face", use_container_width=True):
                student_name = student_name.strip()
                student_id = student_id.strip()
                image = st.session_state.get("student_face_image")

                if not student_name or not student_id:
                    st.warning("Please enter both your name and student ID.")
                elif not student_id.isdigit():
                    st.warning("Student ID must be a valid number.")
                elif image is None:
                    st.warning("Please capture your face with the camera first.")
                elif not check_student_exist(student_id):
                    st.error(f"Student ID {student_id} already exists in the system.")
                else:
                    with st.spinner("Processing face embedding and saving..."):
                        embeddings = process_image(image)

                        if not embeddings:
                            st.error("No clear face detected in the photo. Please center your face and ensure good lighting.")
                        else:
                            embedding = embeddings[0]
                            try:
                                result = create_student(
                                    student_id=student_id,
                                    name=student_name,
                                    embedding=embedding
                                )

                                if result and getattr(result, "data", None):
                                    st.session_state["face_unknown"] = False
                                    st.session_state.pop("face_recognition_failed", None)
                                    st.session_state["reg_success_msg"] = (
                                        f"✅ Face registered successfully for {student_name} (ID: {student_id})! "
                                        "You can now take a photo to verify attendance."
                                    )
                                    st.rerun()
                                else:
                                    st.error("Registration failed. Please try again.")
                            except Exception as e:
                                st.error(f"Database error during registration: {e}")

    # ===== FOOTER =====
    st.markdown("""
        <div class="footer-text">
            Made with 💜 for smarter attendance · AttendX
        </div>
    """, unsafe_allow_html=True)