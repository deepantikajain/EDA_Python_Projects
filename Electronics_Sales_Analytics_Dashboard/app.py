import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(
    page_title="Electronics Sales Analytics Dashboard",
    layout="wide"
)


st.markdown("""
<style>

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #1e242c, #2b323c);
}


[data-testid="stSidebar"] {
    background: #1a1f26;
}


h1 {
    color: #d6d9de;
}
h2, h3, h4 {
    color: #cfd4da;
}


p, label, span {
    color: #b8bec6;
}
</style>
""", unsafe_allow_html=True)





st.markdown("""
<style>
[data-testid="metric-container"] {
    background-color: white;
    border-radius: 12px;
    padding: 15px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("sales_data.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

st.sidebar.title("🎯 Filters")

region_filter = st.sidebar.multiselect(
    "Select Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

product_filter = st.sidebar.multiselect(
    "Select Product",
    df["Product"].unique(),
    default=df["Product"].unique()
)

filtered_df = df[
    (df["Region"].isin(region_filter)) &
    (df["Product"].isin(product_filter))
]


st.title("📊 Electronics Sales Analytics Dashboard")
st.caption("Interactive dashboard with KPIs and Exploratory Data Analysis")


total_revenue = filtered_df["Revenue"].sum()
total_units = filtered_df["Units_Sold"].sum()
avg_units = filtered_df["Units_Sold"].mean()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Revenue", f"₹{total_revenue:,}")
col2.metric("📦 Total Units Sold", total_units)
col3.metric("📈 Avg Units per Day", f"{avg_units:.2f}")

st.markdown("---")


col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue by Product")
    fig, ax = plt.subplots(figsize=(5, 3))
    revenue_product = filtered_df.groupby("Product")["Revenue"].sum()
    sns.barplot(x=revenue_product.index, y=revenue_product.values, ax=ax)
    ax.set_ylabel("Revenue")
    ax.set_xlabel("Product")
    st.pyplot(fig)

# Units Sold Over Time
with col2:
    st.subheader("Units Sold Over Time")
    fig, ax = plt.subplots(figsize=(5, 3))
    units_time = filtered_df.groupby("Date")["Units_Sold"].sum()
    ax.plot(units_time.index, units_time.values, marker="o")
    ax.set_ylabel("Units Sold")
    ax.set_xlabel("Date")
    st.pyplot(fig)

st.markdown("---")


st.subheader("📊 Exploratory Data Analysis")

col1, col2 = st.columns(2)

with col1:
    st.write("Revenue Distribution")
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.histplot(filtered_df["Revenue"], kde=True, ax=ax)
    st.pyplot(fig)


with col2:
    st.write("Revenue by Region")
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.boxplot(x="Region", y="Revenue", data=filtered_df, ax=ax)
    st.pyplot(fig)


st.subheader("Correlation Heatmap")
fig, ax = plt.subplots(figsize=(6, 3))
corr = filtered_df[["Revenue", "Units_Sold"]].corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)

st.markdown("---")

st.subheader("📋 Sales Data")
st.dataframe(
    filtered_df.sort_values(by="Date", ascending=False),
    use_container_width=True
)

