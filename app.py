# --- Import libraries ---
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load data
df = pd.read_csv('cleaned_indicators_lka.csv')

# Page config 
st.set_page_config(page_title="Sri Lanka Indicators Dashboard", page_icon="🇱🇰", layout="wide")

# Sidebar Navigation (About first) 
page = st.sidebar.selectbox("Navigation", ["About", "Home", "Advanced Analysis"])

# About Page
if page == "About":
    st.title("📚 About this Dashboard")
    st.image(
    "https://cdn-wordpress-info.futurelearn.com/wp-content/uploads/how-does-the-economy-work-606x303.jpg.webp",  
    use_column_width=True
    )

    st.markdown("""
    ## 🇱🇰 Sri Lanka Economic and Social Indicators Dashboard

    This dashboard visualises economic and social indicators for Sri Lanka between 2000 and 2023.
    It provides interactive tools to explore historical data trends, relationships between different indicators, and advanced statistical analyses.

    ### Key Features:
    - 📈 Interactive line charts and comparisons
    - 🧮 KPI metrics summary
    - 📊 Univariate, Bivariate and Multivariate analysis
    - 🗃️ Raw data exploration
    - 🔥 Correlation heatmaps for multivariate insights

    ### About the Dataset:
    The dataset used in this project is the **World Bank Combined Indicators for Sri Lanka**, publicly available from the Humanitarian Data Exchange (HDX).
    
    #### Key Highlights:
    - Covers economic, health, education, infrastructure, and environmental indicators
    - Time span: 2000 to 2023
    - Includes GDP, Inflation, Exports, Imports, FDI, Life Expectancy, Population Growth, Energy Use, and more
    - Collected and maintained by the World Bank for reliability and global standards
    
    This dataset provides a comprehensive view of Sri Lanka’s socio-economic trends, useful for researchers, students, and policymakers.

    **Source:** [World Bank Combined Indicators for Sri Lanka (HDX)](https://data.humdata.org/dataset/world-bank-combined-indicators-for-sri-lanka)

    ### Built With:
    - Python 🐍
    - Streamlit 🚀
    - Plotly 📈
    - Pandas 🐼

    **Author:** Imara Riyal
    """)

# Home Page 
if page == "Home":
    # Sidebar filters
    st.sidebar.title("Filters")
    all_indicators = df['Indicator'].unique()

    selected_indicators = st.sidebar.multiselect(
        "Select Indicators:",
        options=all_indicators,
        default=list(all_indicators)[:5]
    )

    year_range = st.sidebar.slider(
        "Select Year Range:",
        min_value=int(df['Year'].min()),
        max_value=int(df['Year'].max()),
        value=(2000, 2023)
    )

    # Filter data
    filtered_df = df[
        (df['Indicator'].isin(selected_indicators)) &
        (df['Year'] >= year_range[0]) &
        (df['Year'] <= year_range[1])
    ]

    # Page title
    st.title("🇱🇰 Sri Lanka Economic & Social Indicators Dashboard")
    st.markdown("Explore Sri Lanka's key indicators over time.")

    # Tabs
    tab1, tab2, tab3 = st.tabs(["Line Charts", "Comparative Analysis", "Indicators Deep Dive"])

    # --- Tab 1: Line Charts ---
    with tab1:
        st.header("Trend Analysis")
        for indicator in selected_indicators:
            indicator_df = filtered_df[filtered_df['Indicator'] == indicator]
            fig = px.line(indicator_df, x='Year', y='Value', title=indicator, markers=True)
            fig.update_layout(hovermode='x unified')
            st.plotly_chart(fig, use_container_width=True)

    # Tab 2: Comparative Analysis 
    with tab2:
        st.header("Comparative Analysis")
        if len(selected_indicators) >= 2:
            fig = make_subplots(
                rows=len(selected_indicators), cols=1,
                shared_xaxes=True, subplot_titles=selected_indicators,
                vertical_spacing=0.05
            )

            for i, indicator in enumerate(selected_indicators, start=1):
                indicator_df = filtered_df[filtered_df['Indicator'] == indicator]
                fig.add_trace(
                    go.Scatter(x=indicator_df['Year'], y=indicator_df['Value'],
                               mode='lines+markers', name=indicator),
                    row=i, col=1
                )

            fig.update_layout(height=300 * len(selected_indicators), showlegend=False, hovermode='x unified')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Please select at least two indicators.")

    # Tab 3: Indicators Deep Dive 
    with tab3:
        st.header("Indicators Deep Dive")

        if not filtered_df.empty:
            st.subheader("Selected Indicators Overview")
            fig = px.line(
                filtered_df,
                x='Year',
                y='Value',
                color='Indicator',
                markers=True,
                title="Multiple Indicators Over Time"
            )
            fig.update_layout(hovermode='x unified')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data available for selected filters.")

    # KPIs
    st.markdown("---")
    st.subheader("Key Metrics")

    if not filtered_df.empty:
        latest_year = filtered_df['Year'].max()
        latest_data = filtered_df[filtered_df['Year'] == latest_year]

        cols = st.columns(min(3, len(latest_data)))

        for idx, (col, row) in enumerate(zip(cols, latest_data.itertuples())):
            col.metric(
                label=f"{row.Indicator} ({int(row.Year)})",
                value=f"{row.Value:,.2f}"
            )
    else:
        st.info("No data to show KPIs.")

    # Raw Data 
    st.markdown("---")
    st.subheader("Raw Data Table")
    st.dataframe(filtered_df.sort_values(['Indicator', 'Year']), use_container_width=True)

# Advanced Analysis Page
if page == "Advanced Analysis":
    st.title("📊 Advanced Data Analysis")

    # Univariate
    st.subheader("Univariate Analysis: Distributions")
    selected_uni = st.multiselect(
        "Select indicators for Univariate Analysis",
        options=df['Indicator'].unique(),
        default=list(df['Indicator'].unique())[:3]
    )

    for indicator in selected_uni:
        uni_df = df[df['Indicator'] == indicator]
        fig = px.histogram(uni_df, x='Value', nbins=30, title=f"Distribution of {indicator}")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Bivariate
    st.subheader("Bivariate Analysis: Scatter Plot between Two Indicators")

    col1, col2 = st.columns(2)
    with col1:
        x_indicator = st.selectbox("Select X-axis Indicator:", options=df['Indicator'].unique())
    with col2:
        y_indicator = st.selectbox("Select Y-axis Indicator:", options=df['Indicator'].unique())

    x_df = df[df['Indicator'] == x_indicator]
    y_df = df[df['Indicator'] == y_indicator]

    merged = pd.merge(x_df, y_df, on='Year', suffixes=('_X', '_Y'))

    if not merged.empty:
        fig = px.scatter(
            merged, x='Value_X', y='Value_Y', trendline='ols',
            labels={'Value_X': x_indicator, 'Value_Y': y_indicator},
            title=f"{x_indicator} vs {y_indicator}"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Multivariate
    st.subheader("Multivariate Analysis: Correlation Heatmap")
    selected_multi = st.multiselect(
        "Select indicators for Multivariate Analysis",
        options=df['Indicator'].unique(),
        default=list(df['Indicator'].unique())[:5]
    )

    multi_df = df[df['Indicator'].isin(selected_multi)]
    pivot_multi = multi_df.pivot(index='Year', columns='Indicator', values='Value')
    corr = pivot_multi.corr()

    if not corr.empty:
        fig = px.imshow(corr, text_auto=True, color_continuous_scale='RdBu_r', title="Correlation Matrix")
        st.plotly_chart(fig, use_container_width=True)
