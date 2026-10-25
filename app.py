import streamlit as st 
from src.screens.login_screen import login_screen
from src.screens.teacher_screens import teacher_screen, teacher_dashboard
from src.screens.students_screens import student_screen, student_dashboard
from src.screens.home_screens import home_screen


def main():
    if "login_state" not in st.session_state:
        st.session_state["login_state"] = None
    
    match st.session_state["login_state"]:
        case "Teacher":
            teacher_screen()
        case "Student":
            student_screen()
        case "Student_Dashboard":
            student_dashboard()
        case "Login":
            login_screen()
        case "Dashboard":
            # Reached after successful login from login_screen
            if st.session_state.get("teacher_user"):
                teacher_dashboard(st.session_state["teacher_user"])
            else:
                st.session_state["login_state"] = "Login"
                st.rerun()
        case None:
            home_screen()

if __name__ == "__main__":
    main()


    