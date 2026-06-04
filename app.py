import streamlit as st
import pandas as pd
import plotly.express as px

# Page Settings
st.set_page_config(
    page_title="AI Student Impact Dashboard",
    page_icon="🎓",
    layout="wide"
)

# Load Dataset
df = pd.read_csv("ai_student_impact_dataset.csv")

# Title
st.title("🎓 AI Student Impact Analysis Dashboard")
st.markdown("Analyze the impact of AI usage on students.")

# Sidebar Filters
st.sidebar.header("Filters")

for col in df.select_dtypes(include="object").columns:
    options = st.sidebar.multiselect(
        col,
        df[col].unique(),
        default=df[col].unique()
    )
    df = df[df[col].isin(options)]

# KPI Section
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Students", len(df))

numeric_cols = df.select_dtypes(include="number").columns

if len(numeric_cols) > 0:
    col2.metric(
        "Average Score",
        round(df[numeric_cols[0]].mean(), 2)
    )

    col3.metric(
        "Maximum Score",
        round(df[numeric_cols[0]].max(), 2)
    )

# Dataset Preview
st.subheader("Dataset Preview")
st.dataframe(df)

# Charts
st.subheader("📈 Visual Analytics")

if len(numeric_cols) >= 2:

    fig1 = px.scatter(
        df,
        x=numeric_cols[0],
        y=numeric_cols[1],
        title=f"{numeric_cols[0]} vs {numeric_cols[1]}"
    )

    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.histogram(
        df,
        x=numeric_cols[0],
        title=f"Distribution of {numeric_cols[0]}"
    )

    st.plotly_chart(fig2, use_container_width=True)

# Correlation Heatmap
if len(numeric_cols) > 1:

    st.subheader("🔥 Correlation Analysis")

    corr = df[numeric_cols].corr()

    fig3 = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        title="Correlation Matrix"
    )

    st.plotly_chart(fig3, use_container_width=True)

# Insights
st.subheader("💡 Insights")

if len(numeric_cols) > 0:

    highest_avg = df[numeric_cols].mean().idxmax()

    st.success(
        f"Highest average metric: {highest_avg}"
    )

    st.info(
        f"Dataset contains {len(df)} student records."
    )

# Footer
st.markdown("---")
st.caption("Built with Streamlit & Python")
