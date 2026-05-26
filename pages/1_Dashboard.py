import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Dashboard | Credit Risk",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------------------
# SAME THEME AS MAIN APP
# ---------------------------------------------------

st.markdown("""
<style>

html, body, [class*="css"], .stApp {
    background-color: #F4F7FB;
    color: #0F172A;
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1px solid #E2E8F0 !important;
}

[data-testid="stSidebar"] * {
    color: #0F172A !important;
}

section[data-testid="stSidebarNav"] * {
    color: #0F172A !important;
}

/* MAIN */

.block-container {
    padding-top: 2rem;
    max-width: 1450px;
}

/* METRIC CARDS */

div[data-testid="metric-container"] {
    background: white;
    border: 1px solid #E2E8F0;
    padding: 1rem;
    border-radius: 16px;
}

/* DATAFRAME */

[data-testid="stDataFrame"] {
    background: white !important;
}

/* PLOTLY TEXT */

.js-plotly-plot .plotly text {
    fill: #0F172A !important;
}

/* HIDE STREAMLIT */

#MainMenu, footer, header {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("Risk Analytics Dashboard")

st.caption(
    "Portfolio-level analytics and applicant monitoring"
)

st.divider()

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

if not os.path.exists("data/prediction_logs.csv"):

    st.warning("No prediction logs found yet.")
    st.stop()

df = pd.read_csv("data/prediction_logs.csv")

if len(df) == 0:

    st.warning("No predictions available.")
    st.stop()

# ---------------------------------------------------
# METRICS
# ---------------------------------------------------

total_apps = len(df)

approval_rate = (
    (df["decision"]
     .str.contains("APPROVE"))
     .mean() * 100
)

rejection_rate = (
    (df["decision"]
     .str.contains("REJECT"))
     .mean() * 100
)

avg_risk = (
    df["probability"].mean() * 100
)

m1, m2, m3, m4 = st.columns(4)

m1.metric(
    "Total Applications",
    f"{total_apps}"
)

m2.metric(
    "Approval Rate",
    f"{approval_rate:.1f}%"
)

m3.metric(
    "Rejection Rate",
    f"{rejection_rate:.1f}%"
)

m4.metric(
    "Avg Default Risk",
    f"{avg_risk:.1f}%"
)

# ---------------------------------------------------
# CHARTS
# ---------------------------------------------------

c1, c2 = st.columns(2)

# Risk Distribution

with c1:

    st.markdown("""
    <div class="chart-card">
    """, unsafe_allow_html=True)

    risk_counts = df["risk"].value_counts()

    fig1 = px.pie(
        names=risk_counts.index,
        values=risk_counts.values,
        hole=0.55
    )

    fig1.update_layout(
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(
        color="#0F172A",
        size=14
    ),
    height=400
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

# Probability Distribution

with c2:

    st.markdown("""
    <div class="chart-card">
    """, unsafe_allow_html=True)

    fig2 = px.histogram(
        df,
        x="probability",
        nbins=20
    )

    fig2.update_layout(
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(
        color="#0F172A",
        size=14
    ),
    xaxis=dict(
        color="#0F172A"
    ),
    yaxis=dict(
        color="#0F172A"
    ),
    height=400
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# RECENT APPLICATIONS
# ---------------------------------------------------

st.markdown("## Recent Applications")

show_df = df.tail(10).copy()

show_df["probability"] = (
    show_df["probability"] * 100
).round(2)

st.dataframe(
    show_df,
    use_container_width=True
)