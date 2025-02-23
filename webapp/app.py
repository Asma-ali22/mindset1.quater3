

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

# Streamlit page config
st.set_page_config(page_title="Student Performance Analyzer", layout="wide")
st.title("📈 Student Performance Analyzer")
st.write("Analyze students' academic performance with visual insights and data cleaning!")

# File uploader
uploaded_file = st.file_uploader("Upload Student Data File (CSV or Excel):", type=["csv", "xlsx"])

if uploaded_file:
    # Read file based on extension
    file_ext = uploaded_file.name.split('.')[-1]
    if file_ext == "csv":
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Preview of Student Data")
    st.dataframe(df.head())

    # Data Info
    st.write(f"**Total Students:** {df.shape[0]}")
    st.write(f"**Total Columns:** {df.shape[1]}")

    # Data Cleaning
    st.subheader("🧹 Data Cleaning Options")
    if st.checkbox("Remove Duplicate Records"):
        df.drop_duplicates(inplace=True)
        st.success("Duplicates removed successfully!")

    if st.checkbox("Fill Missing Values (Numerical)"):
        numeric_cols = df.select_dtypes(include=['number']).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        st.success("Missing values filled with mean values.")

    # Statistical Summary
    st.subheader("📊 Statistical Summary")
    st.write(df.describe())

    # Visualization
    st.subheader("🎨 Visualize Student Performance")
    if st.checkbox("Show Subject-wise Average Marks (Bar Chart)"):
        avg_marks = df.select_dtypes(include=['number']).mean()
        fig, ax = plt.subplots()
        avg_marks.plot(kind='bar', ax=ax, color='skyblue')
        ax.set_ylabel("Average Marks")
        ax.set_title("Subject-wise Average Marks")
        st.pyplot(fig)

    if st.checkbox("Show Pass/Fail Distribution (Pie Chart)"):
        if 'Total Marks' in df.columns:
            df['Status'] = df['Total Marks'].apply(lambda x: 'Pass' if x >= 40 else 'Fail')
            status_counts = df['Status'].value_counts()

            fig, ax = plt.subplots()
            ax.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=90)
            ax.set_title("Pass vs Fail Distribution")
            st.pyplot(fig)
        else:
            st.warning("Column 'Total Marks' not found for Pass/Fail analysis.")

    # Data Export
    st.subheader("💾 Export Processed Data")
    file_format = st.radio("Choose file format for download:", ["CSV", "Excel"])
    buffer = BytesIO()

    if file_format == "CSV":
        df.to_csv(buffer, index=False)
        mime_type = "text/csv"
        file_name = "Processed_Student_Data.csv"
    else:
        df.to_excel(buffer, index=False)
        mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        file_name = "Processed_Student_Data.xlsx"

    buffer.seek(0)
    st.download_button(
        label="Download Processed Data",
        data=buffer,
        file_name=file_name,
        mime=mime_type,
    )
    st.success("Data ready for download!")
