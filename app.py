# --- Import libraries ---
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- Load dataset ---
df= pd.read_csv('cleaned_indicators_lka.csv')


# --- Streamlit page config ---
st.set_page_config(page_title="Sri Lanka Indicators Dashboard", page_icon="🇱🇰", layout="wide")

# --- Sidebar Navigation ---
page = st.sidebar.selectbox("Navigation", ["Home", "Advanced Analysis", "About"])

# --- Home Page ---
if page == "Home":
    # --- Sidebar filters ---
    st.sidebar.title("Filters")
    selected_indicators = st.sidebar.multiselect(
        "Select Indicators:",
        options=df['Indicator'].unique(),
        default=[
            "GDP (current US$)",
            "Inflation, consumer prices (annual %)",
            "Life expectancy at birth, female (years)",
            "Life expectancy at birth, male (years)"
        ]
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

    # --- Page title ---
    st.title("🇱🇰 Sri Lanka Economic & Social Indicators Dashboard")
    st.markdown("Explore key economic and social trends for Sri Lanka from 2000 to 2023.")

    # --- Tabs for analysis ---
    tab1, tab2, tab3 = st.tabs(["Line Charts", "Comparative Analysis", "Economic Indicators Deep Dive"])

    # --- Tab 1: Line Charts ---
    with tab1:
        st.header("Trend Analysis")
        for indicator in selected_indicators:
            indicator_df = filtered_df[filtered_df['Indicator'] == indicator]
            fig = px.line(
                indicator_df, x='Year', y='Value', title=indicator, markers=True
            )
            fig.update_layout(hovermode='x unified')
            st.plotly_chart(fig, use_container_width=True)

    # --- Tab 2: Comparative Analysis ---
    with tab2:
        st.header("Comparative Analysis")
        if len(selected_indicators) >= 2:
            fig = make_subplots(
                rows=len(selected_indicators), cols=1, shared_xaxes=True,
                subplot_titles=selected_indicators, vertical_spacing=0.05
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

    # --- Tab 3: Economic Indicators Deep Dive ---
    with tab3:
        st.header("Economic Indicators Deep Dive")
        economic_indicators = [
            "GDP (current US$)",
            "Inflation, consumer prices (annual %)",
            "Foreign direct investment, net inflows (BoP, current US$)",
            "Trade in services (% of GDP)",
            "Exports of goods and services (current US$)",
            "Imports of goods and services (current US$)"
        ]

        econ_df = filtered_df[filtered_df['Indicator'].isin(economic_indicators)]

        if not econ_df.empty:
            # GDP vs Inflation
            st.subheader("GDP vs Inflation")
            gdp_df = econ_df[econ_df['Indicator'] == "GDP (current US$)"]
            inflation_df = econ_df[econ_df['Indicator'] == "Inflation, consumer prices (annual %)"]

            if not gdp_df.empty and not inflation_df.empty:
                fig = make_subplots(specs=[[{"secondary_y": True}]])
                fig.add_trace(go.Bar(x=gdp_df['Year'], y=gdp_df['Value'], name="GDP"), secondary_y=False)
                fig.add_trace(go.Scatter(x=inflation_df['Year'], y=inflation_df['Value'], 
                                         name="Inflation", mode='lines+markers', line=dict(color='red')), secondary_y=True)
                fig.update_layout(title="GDP and Inflation Over Time", hovermode='x unified')
                st.plotly_chart(fig, use_container_width=True)

            # Trade Indicators
            st.subheader("Trade Indicators")
            trade_df = econ_df[econ_df['Indicator'].isin([
                "Trade in services (% of GDP)",
                "Exports of goods and services (current US$)",
                "Imports of goods and services (current US$)"
            ])]
            if not trade_df.empty:
                fig = px.line(trade_df, x='Year', y='Value', color='Indicator', markers=True)
                fig.update_layout(hovermode='x unified')
                st.plotly_chart(fig, use_container_width=True)

            # Foreign Direct Investment
            st.subheader("Foreign Direct Investment (FDI)")
            fdi_df = econ_df[econ_df['Indicator'] == "Foreign direct investment, net inflows (BoP, current US$)"]
            if not fdi_df.empty:
                fig = px.bar(fdi_df, x='Year', y='Value', title="FDI Over Time")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No economic indicators selected.")

    # --- KPIs Section ---
    st.markdown("---")
    st.subheader("Key Metrics")

    col1, col2, col3 = st.columns(3)
    try:
        latest_gdp = df[df['Indicator'] == "GDP (current US$)"].sort_values('Year').iloc[-1]
        latest_inflation = df[df['Indicator'] == "Inflation, consumer prices (annual %)"].sort_values('Year').iloc[-1]
        latest_life_female = df[df['Indicator'] == "Life expectancy at birth, female (years)"].sort_values('Year').iloc[-1]

        col1.metric(f"GDP ({int(latest_gdp['Year'])})", f"${latest_gdp['Value']:,.2f}")
        col2.metric(f"Inflation ({int(latest_inflation['Year'])})", f"{latest_inflation['Value']:.2f}%")
        col3.metric(f"Female Life Expectancy ({int(latest_life_female['Year'])})", f"{latest_life_female['Value']:.1f} years")
    except Exception as e:
        st.error("Error loading key metrics.")

    # --- Raw Data ---
    st.markdown("---")
    st.subheader("Raw Data")
    st.dataframe(filtered_df.sort_values(['Indicator', 'Year']), use_container_width=True)

# --- Advanced Analysis Page ---
if page == "Advanced Analysis":
    st.title("📊 Advanced Data Analysis")

    # Univariate
    st.subheader("Univariate Analysis: Distributions")
    selected_uni = st.multiselect(
        "Select indicators for Univariate Analysis",
        options=df['Indicator'].unique(),
        default=["GDP (current US$)", "Inflation, consumer prices (annual %)"]
    )

    for indicator in selected_uni:
        uni_df = df[df['Indicator'] == indicator]
        fig = px.histogram(uni_df, x='Value', nbins=30, title=f"Distribution of {indicator}")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Bivariate
    st.subheader("Bivariate Analysis: GDP vs Inflation")
    gdp_df = df[df['Indicator'] == "GDP (current US$)"]
    inflation_df = df[df['Indicator'] == "Inflation, consumer prices (annual %)"]
    
    if not gdp_df.empty and not inflation_df.empty:
        merged_df = pd.merge(gdp_df, inflation_df, on='Year', suffixes=('_GDP', '_Inflation'))
        fig = px.scatter(merged_df, x='Value_GDP', y='Value_Inflation', trendline='ols',
                         labels={"Value_GDP": "GDP (US$)", "Value_Inflation": "Inflation (%)"},
                         title="GDP vs Inflation Scatter Plot")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Multivariate
    st.subheader("Multivariate Analysis: Correlation Heatmap")
    multi_df = df[df['Indicator'].isin([
        "GDP (current US$)", 
        "Inflation, consumer prices (annual %)",
        "Foreign direct investment, net inflows (BoP, current US$)",
        "Exports of goods and services (current US$)",
        "Imports of goods and services (current US$)"
    ])]

    pivot_df = multi_df.pivot(index='Year', columns='Indicator', values='Value')
    corr_matrix = pivot_df.corr()

    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale='RdBu_r',
        title="Correlation Matrix of Economic Indicators"
    )
    st.plotly_chart(fig, use_container_width=True)

# --- About Page ---
if page == "About":
    st.title("📚 About this Project")
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Coat_of_arms_of_Sri_Lanka.svg/1200px-Coat_of_arms_of_Sri_Lanka.svg.png", width=150)
    st.markdown("""
    **Sri Lanka Economic and Social Indicators Dashboard** 🇱🇰

    This dashboard visualizes key economic and social indicators for Sri Lanka, using World Bank data from 2000 to 2023.

    - Analyze trends in GDP, Inflation, Trade, and Life Expectancy
    - Perform Univariate, Bivariate, and Multivariate analysis
    - Support evidence-based decision making

    **Built With:**  
    - Python 🐍  
    - Streamlit 🚀  
    - Plotly 📈  

    **Author:** Your Name  
    **Dataset Source:** [World Bank Combined Indicators for Sri Lanka (HDX)](https://data.humdata.org/dataset/world-bank-combined-indicators-for-sri-lanka)
    """)
