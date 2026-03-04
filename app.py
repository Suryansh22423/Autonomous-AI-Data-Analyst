# app.py - UI for Autonomous AI Data Analyst
import streamlit as st
import pandas as pd
from tools import load_csv, show_head, calculate_stats, correlation, generate_plot
from agent import process_nlp_query

st.set_page_config(page_title="Autonomous AI Data Analyst", layout="wide")

st.title("🚀 Autonomous AI Data Analyst with NLP")

# Upload CSV
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file is not None:
    data_info = load_csv(uploaded_file)
    st.success(f"Data loaded: {data_info}")
    st.dataframe(show_head())

# User query input
query = st.text_input("Ask a question or type a command (e.g., correlation, stats, plot)")

if st.button("Submit") and query:
    if uploaded_file is None:
        st.warning("Please upload a CSV first!")
    else:
        # Use NLP processing from agent
        result = process_nlp_query(query)
        
        # Display numeric or textual results
        if isinstance(result, pd.DataFrame):
            st.dataframe(result)
        elif isinstance(result, dict):
            st.json(result)
        else:
            st.write(result)

# Plot example: show saved plots
st.markdown("---")
st.subheader("Generated Plots")
import os
plot_files = [f for f in os.listdir() if f.endswith(".png")]
for plot_file in plot_files:
    st.image(plot_file, caption=plot_file)