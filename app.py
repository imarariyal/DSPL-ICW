# Import libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned dataset
df = pd.read_csv('cleaned_indicators_lka.csv')

# Sidebar - Title
st.sidebar.title("Sri Lanka Economy Dashboard")

# Sidebar - Indicator selection
indicator_options = df['Indicator'].unique()
selected_indicator = st.sidebar.selectbox("Select Indicator:", indicator_options)

# Sidebar - Year selection
min_year = int(df['Year'].min())
max_year = int(df['Year'].max())
year_range = st.sidebar.slider("Select Year Range:", min_year, max_year, (min_year, max_year))

# Filter data based on user selection
df_filtered = df[
    (df['Indicator'] == selected_indicator) &
    (df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])
]

# Main - Title
st.title(f"Sri Lanka {selected_indicator} Analysis")

# KPIs
st.metric("Latest Value", f"{df_filtered.sort_values('Year').iloc[-1]['Value']:.2f}")
st.metric("Average Value", f"{df_filtered['Value'].mean():.2f}")

# Main - Line Chart
st.subheader(f"{selected_indicator} over Time")
fig, ax = plt.subplots()
ax.plot(df_filtered['Year'], df_filtered['Value'], marker='o')
ax.set_xlabel("Year")
ax.set_ylabel(selected_indicator)
ax.grid(True)
st.pyplot(fig)

# Optional: Show raw data
with st.expander("Show Raw Data"):
    st.dataframe(df_filtered)