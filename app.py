# Import libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned dataset
df = pd.read_csv('cleaned_indicators_lka.csv')

# Sidebar - Title
st.sidebar.title("Sri Lanka Economy Dashboard")

# Sidebar - Indicator selection
indicator_options = df['Indicator Name'].unique()
selected_indicator = st.sidebar.selectbox("Select Indicator:", indicator_options)

# Sidebar - Year selection
min_year = int(df['Year'].min())
max_year = int(df['Year'].max())
year_range = st.sidebar.slider("Select Year Range:", min_year, max_year, (min_year, max_year))




