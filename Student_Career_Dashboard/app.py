import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from student_result import student_result_dashboard
from resume_builder import resume_builder
from career_recommendation import career_recommendation_system

st.set_page_config(page_title="Student Career Dashboard", layout="wide")

# 🌑 DARK DASHBOARD THEME
st.markdown("""
<style>

/* MAIN BACKGROUND */
.stApp {
    background: linear-gradient(135deg, #020617, #020617);
    color: white;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617, #020617);
    border-right: 1px solid #1e293b;
}

/* CARDS */
.card {
    background: rgba(255, 255, 255, 0.05);
    padding: 14px;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 6px 20px rgba(0,0,0,0.4);
    margin-bottom: 12px;
}

/* KPI CARDS */
.kpi {
    background: rgba(255,255,255,0.06);
    padding: 12px;
    border-radius: 12px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.08);
}

/* TEXT */
h1, h2, h3, h4, h5, h6, p, span {
    color: #e5e7eb !important;
}

.small-text {
    font-size: 13px;
    color: #9ca3af;
}

</style>
""", unsafe_allow_html=True)

st.title("🎓 Student Career Analytics Dashboard")

menu = st.sidebar.selectbox(
    "Select Module",
    ["Home", "Student Result Dashboard", "Resume Builder", "Career Recommendation System"]
)

# 🏠 HOME DASHBOARD
if menu == "Home":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🏠 Overview")
    st.write("A data-driven platform to analyze student performance, skills, and career paths.")
    st.markdown("</div>", unsafe_allow_html=True)

    # KPI CARDS
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<div class='kpi'>📊 <br><b>Performance Analytics</b></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='kpi'>💼 <br><b>Skill & Resume Analysis</b></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='kpi'>🎯 <br><b>Career Recommendation</b></div>", unsafe_allow_html=True)

elif menu == "Student Result Dashboard":
    student_result_dashboard()

elif menu == "Resume Builder":
    resume_builder()

elif menu == "Career Recommendation System":
    career_recommendation_system()
