import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def resume_builder():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("💼 LinkedIn-Style Profile & Skill Analytics")

    col1, col2 = st.columns([2, 1])

    with col1:
        name = st.text_input("Name", "Your Name")
        role = st.text_input("Role", "Aspiring Developer")
        location = st.text_input("Location", "Your City")

    with col2:
        email = st.text_input("Email", "your@email.com")

    summary = st.text_area(
        "About / Summary",
        "A passionate student interested in technology, data, and development."
    )

    st.markdown("### 🛠️ Skills")

    skills = ["Python", "SQL", "HTML", "CSS", "JavaScript", "Data Analysis"]
    skill_levels = {skill: st.slider(skill, 0, 10, 5) for skill in skills}

    if st.button("Generate Profile"):
        df = pd.DataFrame(skill_levels.items(), columns=["Skill", "Level"])

        # PROFILE CARD
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        left, right = st.columns([3, 2])

        with left:
            st.markdown(f"### {name}")
            st.markdown(f"**{role}**")
            st.markdown(f"<span class='small-text'>📍 {location} | 📧 {email}</span>", unsafe_allow_html=True)
            st.markdown("#### About")
            st.write(summary)

        with right:
            st.markdown("#### Skills Data")
            st.dataframe(df, height=160)

        st.markdown("</div>", unsafe_allow_html=True)

        
        fig, ax = plt.subplots(figsize=(3.2, 2.1), dpi=100)
        ax.barh(df["Skill"], df["Level"])
        ax.tick_params(labelsize=7)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=False)

       
        labels = df["Skill"].tolist()
        values = df["Level"].tolist()
        values += values[:1]

        angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
        angles += angles[:1]

        fig2, ax2 = plt.subplots(figsize=(3, 3), dpi=100, subplot_kw=dict(polar=True))
        ax2.plot(angles, values)
        ax2.fill(angles, values, alpha=0.2)
        ax2.set_xticks(angles[:-1])
        ax2.set_xticklabels(labels, fontsize=6)
        st.pyplot(fig2, use_container_width=False)

        # Save for career system
        st.session_state["skills_df"] = df

    st.markdown("</div>", unsafe_allow_html=True)
