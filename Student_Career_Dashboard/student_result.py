import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def student_result_dashboard():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 Student Performance Analytics ")

    # Generic sample subjects
    subjects = ["Math", "Science", "English", "Computer", "AI"]
    marks = []

    cols = st.columns(5)
    for i, sub in enumerate(subjects):
        with cols[i]:
            marks.append(st.number_input(sub, 0, 100, 70))

    if st.button("Analyze Performance"):
        df = pd.DataFrame({"Subject": subjects, "Marks": marks})

        total = df["Marks"].sum()
        avg = df["Marks"].mean()

        
        k1, k2, k3 = st.columns(3)
        with k1:
            st.markdown(f"<div class='kpi'>Total Marks<br><b>{total}</b></div>", unsafe_allow_html=True)
        with k2:
            st.markdown(f"<div class='kpi'>Average<br><b>{avg:.2f}</b></div>", unsafe_allow_html=True)
        with k3:
            grade = "A+" if avg >= 90 else "A" if avg >= 75 else "B" if avg >= 60 else "C" if avg >= 50 else "Fail"
            st.markdown(f"<div class='kpi'>Grade<br><b>{grade}</b></div>", unsafe_allow_html=True)

        st.markdown("### 📊 Data Overview")
        st.dataframe(df)

        # ================= MATPLOTLIB GRAPH =================
        st.markdown("### 📈 Marks Bar Chart ")
        fig, ax = plt.subplots(figsize=(3.2, 2.1), dpi=100)
        ax.bar(df["Subject"], df["Marks"])
        ax.tick_params(labelsize=7)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=False)

        # ================= SEABORN GRAPHS =================

        
        st.markdown("### 📊 Seaborn Barplot")
        fig1, ax1 = plt.subplots(figsize=(3.2, 2.1), dpi=100)
        sns.barplot(x="Subject", y="Marks", data=df, ax=ax1)
        ax1.tick_params(labelsize=7)
        plt.tight_layout()
        st.pyplot(fig1, use_container_width=False)

        
        st.markdown("### 📉 Marks Distribution (Histogram)")
        fig2, ax2 = plt.subplots(figsize=(3.2, 2.1), dpi=100)
        sns.histplot(df["Marks"], bins=5, kde=True, ax=ax2)
        ax2.tick_params(labelsize=7)
        plt.tight_layout()
        st.pyplot(fig2, use_container_width=False)

        
        st.markdown("### 📦 Boxplot (Outlier Detection)")
        fig3, ax3 = plt.subplots(figsize=(3.2, 2.1), dpi=100)
        sns.boxplot(y=df["Marks"], ax=ax3)
        ax3.tick_params(labelsize=7)
        plt.tight_layout()
        st.pyplot(fig3, use_container_width=False)

        
        st.markdown("### 🔥 Correlation Heatmap (EDA)")
        corr = df[["Marks"]].corr()
        fig4, ax4 = plt.subplots(figsize=(3, 2.2), dpi=100)
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax4)
        plt.tight_layout()
        st.pyplot(fig4, use_container_width=False)

        
        st.markdown("### 🔍 EDA Insights")
        st.write("Highest Score:", df.loc[df["Marks"].idxmax(), "Subject"])
        st.write("Lowest Score:", df.loc[df["Marks"].idxmin(), "Subject"])
        st.write("Standard Deviation:", round(df["Marks"].std(), 2))

    st.markdown("</div>", unsafe_allow_html=True)
