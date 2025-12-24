import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Student Dashboard", layout="wide")
st.title("🎓 Student Performance Dashboard with Dynamic Merge")

# ---------- UPLOAD CSV FILES ----------
st.sidebar.subheader("Upload CSV Files")
main_file = st.sidebar.file_uploader("Main CSV", type=["csv"])
secondary_file = st.sidebar.file_uploader("Secondary CSV", type=["csv"])

if main_file and secondary_file:
    main_df = pd.read_csv(main_file)
    secondary_df = pd.read_csv(secondary_file)
    
    main_df.columns = main_df.columns.str.strip()
    secondary_df.columns = secondary_df.columns.str.strip()

    st.subheader("Main Data Preview")
    st.dataframe(main_df.head())
    
    st.subheader("Secondary Data Preview")
    st.dataframe(secondary_df.head())

    # ---------- DYNAMIC MERGE ----------
    join_type = st.radio("Select Join Type", ("inner", "left", "right", "outer"))
    merged_df = pd.merge(main_df, secondary_df, on="student_id", how=join_type)
    st.subheader(f"Merged Data ({join_type} join)")
    st.dataframe(merged_df.head())

    # ---------- FEATURE ENGINEERING ----------
    if 'hours_studied' in merged_df.columns and 'extra_study_hours' in merged_df.columns:
        merged_df['total_study'] = merged_df['hours_studied'] + merged_df['extra_study_hours']

    # ---------- BUTTONS FOR INDIVIDUAL ANALYSIS ----------
    st.subheader("Run Individual Analysis")

    if st.button("Descriptive Statistics"):
        st.write(merged_df.describe())

    if st.button("Histogram of Test Scores"):
        if 'test_score' in merged_df.columns:
            fig = px.histogram(merged_df, x='test_score', color='gender')
            st.plotly_chart(fig, use_container_width=True)

    if st.button("Scatter: Total Study vs Test Score"):
        if 'total_study' in merged_df.columns and 'test_score' in merged_df.columns:
            fig = px.scatter(
                merged_df,
                x='total_study',
                y='test_score',
                color='gender' if 'gender' in merged_df.columns else None,
                size='bonus_points' if 'bonus_points' in merged_df.columns else None,
                hover_data=[col for col in ['attendance_percent','assignments_completed','participation_score'] if col in merged_df.columns]
            )
            st.plotly_chart(fig, use_container_width=True)

    if st.button("Correlation Heatmap"):
        numeric_df = merged_df.select_dtypes(include='number')
        if not numeric_df.empty:
            corr = numeric_df.corr()
            fig = px.imshow(corr, text_auto=True, color_continuous_scale="Viridis")
            st.plotly_chart(fig, use_container_width=True)