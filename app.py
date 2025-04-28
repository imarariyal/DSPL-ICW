import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load cleaned dataset
df = pd.read_csv('cleaned_indicators_lka.csv')

# Set page config
st.set_page_config(
    page_title="Sri Lanka Economic & Social Indicators Dashboard",
    page_icon="🇱🇰",
    layout="wide"
)

# Sidebar filters
st.sidebar.title("Filters")
selected_indicators = st.sidebar.multiselect(
    "Select Indicators to Display",
    options=df['Indicator'].unique(),
    default=[
        "GDP (current US$)",
        "Inflation, consumer prices (annual %)",
        "Life expectancy at birth, female (years)",
        "Life expectancy at birth, male (years)"
    ]
)

year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=int(df['Year'].min()),
    max_value=int(df['Year'].max()),
    value=(2000, 2023)
)

# Main content
st.title("🇱🇰 Sri Lanka Economic & Social Indicators Dashboard")
st.markdown("""
This interactive dashboard visualizes key economic and social indicators for Sri Lanka from 2000 to 2023.
Use the filters in the sidebar to customize the view.
""")

# Filter data based on selections
filtered_df = df[
    (df['Indicator'].isin(selected_indicators)) & 
    (df['Year'] >= year_range[0]) & 
    (df['Year'] <= year_range[1])
]

# Create tabs for different visualizations
tab1, tab2, tab3 = st.tabs(["Line Charts", "Comparative Analysis", "Economic Indicators"])

with tab1:
    st.header("Trend Analysis")
    
    # Create a line chart for each selected indicator
    for indicator in selected_indicators:
        indicator_df = filtered_df[filtered_df['Indicator'] == indicator]
        
        fig = px.line(
            indicator_df,
            x='Year',
            y='Value',
            title=indicator,
            markers=True
        )
        
        # Customize layout
        fig.update_layout(
            xaxis_title='Year',
            yaxis_title='Value',
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Comparative Analysis")
    
    if len(selected_indicators) >= 2:
        # Create a subplot with shared x-axis
        fig = make_subplots(
            rows=len(selected_indicators), 
            cols=1,
            shared_xaxes=True,
            subplot_titles=selected_indicators,
            vertical_spacing=0.05
        )
        
        for i, indicator in enumerate(selected_indicators, 1):
            indicator_df = filtered_df[filtered_df['Indicator'] == indicator]
            
            fig.add_trace(
                go.Scatter(
                    x=indicator_df['Year'],
                    y=indicator_df['Value'],
                    name=indicator,
                    mode='lines+markers'
                ),
                row=i, col=1
            )
        
        fig.update_layout(
            height=300 * len(selected_indicators),
            showlegend=False,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Please select at least 2 indicators for comparison.")

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
    
    # Filter for economic indicators only
    econ_df = filtered_df[filtered_df['Indicator'].isin(economic_indicators)]
    
    if not econ_df.empty:
        # GDP and Inflation comparison
        st.subheader("GDP vs Inflation")
        
        gdp_df = econ_df[econ_df['Indicator'] == "GDP (current US$)"]
        inflation_df = econ_df[econ_df['Indicator'] == "Inflation, consumer prices (annual %)"]
        
        if not gdp_df.empty and not inflation_df.empty:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            # Add GDP trace
            fig.add_trace(
                go.Bar(
                    x=gdp_df['Year'],
                    y=gdp_df['Value'],
                    name="GDP (current US$)",
                    marker_color='blue',
                    opacity=0.6
                ),
                secondary_y=False
            )
            
            # Add Inflation trace
            fig.add_trace(
                go.Scatter(
                    x=inflation_df['Year'],
                    y=inflation_df['Value'],
                    name="Inflation (%)",
                    mode='lines+markers',
                    line=dict(color='red', width=2)
                ),
                secondary_y=True
            )
            
            fig.update_layout(
                title="GDP and Inflation Over Time",
                xaxis_title="Year",
                yaxis_title="GDP (current US$)",
                yaxis2_title="Inflation (%)",
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Trade indicators
        trade_indicators = [
            "Trade in services (% of GDP)",
            "Exports of goods and services (current US$)",
            "Imports of goods and services (current US$)"
        ]
        
        trade_df = econ_df[econ_df['Indicator'].isin(trade_indicators)]
        
        if not trade_df.empty:
            st.subheader("Trade Indicators")
            
            fig = px.line(
                trade_df,
                x='Year',
                y='Value',
                color='Indicator',
                markers=True
            )
            
            fig.update_layout(
                yaxis_title="Value",
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # FDI indicator
        fdi_df = econ_df[econ_df['Indicator'] == "Foreign direct investment, net inflows (BoP, current US$)"]
        
        if not fdi_df.empty:
            st.subheader("Foreign Direct Investment")
            
            fig = px.bar(
                fdi_df,
                x='Year',
                y='Value',
                title="Foreign Direct Investment Over Time"
            )
            
            fig.update_layout(
                yaxis_title="FDI (current US$)",
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No economic indicators selected. Please select some from the sidebar.")

# Add some metrics at the bottom
st.markdown("---")
st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

# Get latest values for some indicators
try:
    latest_gdp = df[df['Indicator'] == "GDP (current US$)"].sort_values('Year').iloc[-1]
    latest_inflation = df[df['Indicator'] == "Inflation, consumer prices (annual %)"].sort_values('Year').iloc[-1]
    latest_life_female = df[df['Indicator'] == "Life expectancy at birth, female (years)"].sort_values('Year').iloc[-1]
    
    with col1:
        st.metric(
            label=f"GDP ({int(latest_gdp['Year'])})",
            value=f"${latest_gdp['Value']:,.2f}",
        )
    
    with col2:
        st.metric(
            label=f"Inflation ({int(latest_inflation['Year'])})",
            value=f"{latest_inflation['Value']:.2f}%",
        )
    
    with col3:
        st.metric(
            label=f"Female Life Expectancy ({int(latest_life_female['Year'])})",
            value=f"{latest_life_female['Value']:.1f} years",
        )
except:
    pass

# Add data table
st.markdown("---")
st.subheader("Raw Data")
st.dataframe(filtered_df.sort_values(['Indicator', 'Year']), use_container_width=True)
