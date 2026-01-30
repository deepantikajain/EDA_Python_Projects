import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def career_recommendation_system():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🎯 Career Match Dashboard")

    if "skills_df" not in st.session_state:
        st.warning("Generate your profile first in Resume Builder.")
        return

    df = st.session_state["skills_df"]

    careers = {
        "Data Analyst": ["Python", "SQL", "Data Analysis"],
        "Full Stack Developer": ["HTML", "CSS", "JavaScript"],
        "DBA": ["SQL", "Python"],
        "AI/ML Engineer": ["Python"],
        "Software Developer": ["Python", "JavaScript"]
    }

    scores = {}
    for career, req in careers.items():
        score = sum(df[df["Skill"].isin(req)]["Level"])
        scores[career] = score

    score_df = pd.DataFrame(scores.items(), columns=["Career", "Score"])
    score_df["Match %"] = (score_df["Score"] / score_df["Score"].max()) * 100

    st.dataframe(score_df.sort_values("Match %", ascending=False), height=200)

    
    fig, ax = plt.subplots(figsize=(3.2, 2.1), dpi=100)
    ax.bar(score_df["Career"], score_df["Match %"])
    ax.tick_params(labelsize=7)
    plt.xticks(rotation=15)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)

    best = score_df.sort_values("Match %", ascending=False).iloc[0]["Career"]
    st.success(f"🔥 Best Career Match: {best}")

    st.markdown("</div>", unsafe_allow_html=True)
