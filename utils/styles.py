import streamlit as st


def load_css():

    st.markdown("""
    <style>

    /* GLOBAL */

    .stApp {
        background-color: #F4F7FB;
    }

    html, body {
        font-family: "Segoe UI", sans-serif;
        color: #0F172A;
    }

    .block-container {
        padding-top: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 1450px;
    }

    /* SIDEBAR */

    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }

    section[data-testid="stSidebar"] * {
        color: #0F172A !important;
    }

    section[data-testid="stSidebar"] label {
        color: #334155 !important;
        font-weight: 500 !important;
        font-size: 0.92rem !important;
    }

    /* MULTIPAGE NAVIGATION */

    section[data-testid="stSidebarNav"] {
        background-color: #FFFFFF !important;
    }

    section[data-testid="stSidebarNav"] * {
        color: #0F172A !important;
        font-weight: 500 !important;
    }

    section[data-testid="stSidebarNav"] a {
        color: #0F172A !important;
    }

    section[data-testid="stSidebarNav"] span {
        color: #0F172A !important;
    }

    /* HEADINGS */

    h1, h2, h3, h4, h5 {
        color: #0F172A !important;
        font-family: "Segoe UI", sans-serif;
        font-weight: 600;
    }

    p, li {
        color: #334155 !important;
    }

    /* HEADER */

    .main-header {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 18px;
        padding: 1.8rem 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
    }

    .main-title {
        font-size: 2rem;
        font-weight: 700;
        color: #0F172A !important;
        margin-bottom: 0.4rem;
    }

    .main-subtitle {
        font-size: 0.95rem;
        color: #64748B !important;
    }

    /* RISK CARD */

    .risk-card {
        padding: 2rem;
        border-radius: 18px;
        margin-bottom: 1rem;
    }

    .risk-low {
        background: #DCFCE7;
        border-left: 6px solid #22C55E;
    }

    .risk-medium {
        background: #FEF3C7;
        border-left: 6px solid #F59E0B;
    }

    .risk-high {
        background: #FEE2E2;
        border-left: 6px solid #EF4444;
    }

    .risk-prob {
        font-size: 4rem;
        font-weight: 700;
        color: #0F172A !important;
        margin: 0.5rem 0;
    }

    .decision {
        font-size: 1.1rem;
        font-weight: 600;
        color: #0F172A !important;
    }

    /* METRICS */

    div[data-testid="metric-container"] {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 1rem;
    }

    div[data-testid="metric-container"] label {
        color: #64748B !important;
    }

    div[data-testid="metric-container"] div {
        color: #0F172A !important;
    }

    /* INPUTS */

    .stSelectbox div,
    .stNumberInput div,
    .stSlider div {
        color: #0F172A !important;
    }

    /* BUTTON */

    .stButton button {
        background: #2563EB;
        color: white !important;
        border: none;
        border-radius: 12px;
        height: 3rem;
        font-weight: 600;
        width: 100%;
    }

    .stButton button:hover {
        background: #1D4ED8;
        color: white !important;
    }

    /* REMOVE STREAMLIT BRANDING */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }
        /* SELECTBOX */

    .stSelectbox div[data-baseweb="select"] {
        background-color: white !important;
        color: #0F172A !important;
    }

    .stSelectbox svg {
        fill: #0F172A !important;
    }

    .stSelectbox input {
        color: #0F172A !important;
    }

    /* DROPDOWN MENU */

    div[role="listbox"] {
        background-color: white !important;
    }

    div[role="option"] {
        color: #0F172A !important;
        background-color: white !important;
    }

    div[role="option"]:hover {
        background-color: #EFF6FF !important;
    }

    </style>
    """, unsafe_allow_html=True)

