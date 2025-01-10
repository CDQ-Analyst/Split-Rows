
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import openpyxl

# Streamlit app title
st.title("Simple Data Analysis App")

# File uploader for CSV files
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    # Read the uploaded CSV file
    data = pd.read_csv(uploaded_file)

    # Display the first few rows of the dataset
    st.subheader("Preview of the Dataset")
    st.dataframe(data.head())

    # Show basic information about the dataset
    st.subheader("Basic Information")
    st.write("Number of Rows:", data.shape[0])
    st.write("Number of Columns:", data.shape[1])

    # Select a column to view statistics
    column = st.selectbox("Select a column to analyze", data.columns)

    if column:
        st.subheader(f"Statistics for {column}")
        st.write(data[column].describe())

    # Plot options
    st.subheader("Visualization")
    plot_type = st.selectbox("Select plot type", ["Histogram", "Line Plot", "Box Plot"])

    if plot_type == "Histogram":
        bins = st.slider("Select number of bins", min_value=5, max_value=50, value=10)
        plt.figure(figsize=(10, 6))
        plt.hist(data[column].dropna(), bins=bins, color='skyblue', edgecolor='black')
        plt.title(f"Histogram of {column}")
        plt.xlabel(column)
        plt.ylabel("Frequency")
        st.pyplot(plt)

    elif plot_type == "Line Plot":
        plt.figure(figsize=(10, 6))
        plt.plot(data[column], color='green')
        plt.title(f"Line Plot of {column}")
        plt.xlabel("Index")
        plt.ylabel(column)
        st.pyplot(plt)

    elif plot_type == "Box Plot":
        plt.figure(figsize=(10, 6))
        plt.boxplot(data[column].dropna(), vert=False, patch_artist=True, boxprops=dict(facecolor='lightblue'))
        plt.title(f"Box Plot of {column}")
        st.pyplot(plt)

    # Save first 10 rows and second 10 rows as .xlsx file
    st.subheader("Save First and Second 10 Rows")
    save_folder = st.text_input("Enter folder path to save the file:")
    if st.button("Save as Excel"):
        if save_folder:
            output_path = Path(save_folder) / "rows_split.xlsx"
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                data.head(10).to_excel(writer, sheet_name='First 10 Rows', index=False)
                data.iloc[10:20].to_excel(writer, sheet_name='Second 10 Rows', index=False)
            st.success(f"File saved successfully at {output_path}")
        else:
            st.error("Please enter a valid folder path.")
else:
    st.info("Please upload a CSV file to get started.")
