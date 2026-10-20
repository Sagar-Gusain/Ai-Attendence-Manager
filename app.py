import streamlit as st 
from src.screens.login_screen import login_screen
from src.screens.teacher_screens import teacher_screen
from src.screens.students_screens import student_screen
from src.screens.home_screens import home_screen


def main():
    if "login_state" not in st.session_state:
        st.session_state["login_state"] = None
    
    match st.session_state["login_state"]:
        case "Teacher":
            teacher_screen()
        case "Student":
            student_screen()
        case None:
            home_screen()

if __name__ == "__main__":
    main()


    