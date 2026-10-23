import streamlit as st


def home_style():
    st.markdown("""
    <style>
        /* Hide the fullscreen button */
        button[title="View fullscreen"] {
            display: none !important;
        }

        /* Hide fullscreen controls by test ID */
        [data-testid="StyledFullScreenButton"] {
            display: none !important;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
        /* Hide Streamlit top bar */
        header[data-testid="stHeader"] {
            display: none;
        }

        /* Hide toolbar */
        [data-testid="stToolbar"] {
            display: none;
        }

        /* Hide menu and footer */
        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        /* Remove extra top spacing */
        .block-container {
            padding-top: 1.5rem !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <style>
    /* Yellow gradient background */
    .stApp {
        background: linear-gradient(135deg, #FDE047, #F59E0B);
        color: #111827;
    }

    /* Teacher and Student buttons */
    .stButton > button {
        background-color: #172554 !important;
        color: #FFFFFF !important;
        border: 2px solid #172554 !important;
        border-radius: 12px;
        padding: 12px 28px;
        min-height: 52px;
        font-size: 18px !important;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    .stButton > button p {
        color: #FFFFFF !important;
    }

    /* Hover effect */
    .stButton > button:hover {
        background-color: #D97706 !important;
        border-color: #FFFFFF !important;
        color: #FFFFFF !important;
        transform: translateY(-2px);
    }

    /* Input fields */
    .stTextInput input {
        background-color: #FFFEF7;
        color: #172554;
        border: 1px solid #EAB308;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

def login_style():
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #FEF9C3, #FACC15);
        color: #111827;
    }
    </style>
    """, unsafe_allow_html=True)


def style_layout():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Boldonse&family=IBM+Plex+Serif:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;1,100;1,200;1,300;1,400;1,500;1,600;1,700&family=Rubik+Storm&display=swap');

    /* Center header section */
    .home-header {
        width: 100%;
        text-align: center;
    }

    /* AttendX title */
    .home-title {
        font-family: 'Rubik Storm', cursive !important;
        font-size: 72px !important;
        font-weight: normal;
        color: #172554 !important;
        text-align: center !important;
        margin: 10px 0 25px 0;
    }

    /* Subtitle */
    .home-subtitle {
        font-family: 'IBM Plex Serif', serif !important;
        font-size: 36px !important;
        color: #172554 !important;
        text-align: center !important;
        margin: 25px 0;
    }

    /* H2 headings */
    h2 {
        font-family: 'IBM Plex Serif', serif !important;
        color: #172554 !important;
    }

    /* H3 headings */
    h3 {
        font-family: 'Boldonse', sans-serif !important;
        color: #92400E !important;
    }

    /* Center images */
    [data-testid="stImage"] {
        display: flex;
        justify-content: center;
    }

    /* Rounded Teacher and Student cards */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFEF7;
        border: 2px solid #FDE68A;
        border-radius: 28px;
        padding: 16px;
        box-shadow: 0 8px 20px rgba(23, 37, 84, 0.12);
    }

    /* Portal card headings */
    .portal-title {
        font-family: 'Boldonse', sans-serif !important;
        font-size: 23px !important;
        color: #172554 !important;
        text-align: center !important;
        margin-bottom: 15px;
    }

    /* Teacher and Student buttons */
    .stButton > button {
        width: 100%;
        min-height: 55px;
        background-color: #172554 !important;
        color: #FFFFFF !important;
        border: 2px solid #172554 !important;
        border-radius: 25px;
        font-size: 17px !important;
        font-weight: 600;
    }

    .stButton > button p {
        color: #FFFFFF !important;
    }

    .stButton > button:hover {
        background-color: #D97706 !important;
        border-color: #FFFFFF !important;
        color: #FFFFFF !important;
    }
    </style>
    """, unsafe_allow_html=True)


def style_background_home():
    st.markdown("""
    <style>
    /* Main page background */
    .stApp {
        background: linear-gradient(135deg, #5865F2, #414BC4) !important;
    }
    
    /* Rounded portal cards */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #E0E3FF !important;
        padding: 2rem !important;
        border-radius: 30px !important;
        border: 2px solid #D6DAFF !important;
        box-shadow: 0 6px 18px rgba(20, 25, 80, 0.15);
    }

    /* Card headings */
    .portal-title {
        font-family: 'Boldonse', sans-serif !important;
        color: #172554 !important;
        font-size: 23px !important;
        text-align: center !important;
        margin-bottom: 16px;
    }

    /* Images */
    [data-testid="stImage"] img {
        object-fit: contain;
        max-height: 220px;
    }

    /* Portal buttons */
    .stButton > button {
        width: 100%;
        background-color: #5865F2 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 25px !important;
        min-height: 48px;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    .stButton > button p {
        color: #FFFFFF !important;
    }

    .stButton > button:hover {
        background-color: #414BC4 !important;
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

def teacher_style():
    st.markdown("""
    <style>
    .stApp {
        background-color: #1E3A8A;
    }

    .container {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem auto;
        max-width: 800px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }

    h2 {
        color: #1E3A8A;
    }

    .stButton > button {
        background-color: #1E3A8A;
        color: white;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)
    