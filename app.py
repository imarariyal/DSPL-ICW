# --- Import libraries ---
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- Page Config ---
st.set_page_config(
    page_title="Sri Lanka Indicators Dashboard",
    page_icon="🇱🇰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Light Mode Plotly Theme ---
px.defaults.template = "plotly_white"

# --- Color Palette (Light Theme) ---
COLOR_PRIMARY = "#4B9CD3"
COLOR_SECONDARY = "#A2D2FF"
COLOR_POSITIVE = "#56C596"
COLOR_WARNING = "#F4A261"
COLOR_NEGATIVE = "#E76F51"
COLOR_TEXT = "#2E2E2E"
COLOR_BG_SECTION = "#F9F9F9"

# --- Load data ---
df = pd.read_csv('cleaned_indicators_lka.csv')

# --- Sidebar Navigation ---
page = st.sidebar.selectbox("📌 Navigation", ["About", "Home", "Advanced Analysis"])

# --- About Page ---
if page == "About":
    st.title("📚 About this Dashboard")
    st.image(
        "https://cdn-wordpress-info.futurelearn.com/wp-content/uploads/how-does-the-economy-work-606x303.jpg.webp",
        use_column_width=True
    )
    st.markdown("""
    ## 🇱🇰 Sri Lanka Economic and Social Indicators Dashboard

    This dashboard visualises key economic and social indicators for Sri Lanka (2000–2023) with interactive tools for analysis.

    ### 🔍 Key Features:
    - 📈 Line charts to track trends
    - 🔁 Indicator comparisons
    - 🧮 KPI summaries
    - 📊 Univariate, bivariate, multivariate visualisations
    - 📁 Raw data access
    - 🔥 Correlation insights

    ### 📊 Dataset:
    - Source: [World Bank via HDX](https://data.humdata.org/dataset/world-bank-combined-indicators-for-sri-lanka)
    - Covers GDP, inflation, exports/imports, life expectancy, and more.
    - Timeframe: 2000 to 2023

    ### 🛠 Built With:
    - Python, Streamlit, Plotly, Pandas

    **Author:** Imara Riyal
    """)

# --- Home Page ---
elif page == "Home":
    st.title("🇱🇰 Sri Lanka Indicators Dashboard")
    st.markdown("Explore Sri Lanka's key economic and social trends over time.")

    # Sidebar filters
    st.sidebar.title("🔎 Filters")
    all_indicators = df['Indicator'].unique()

    selected_indicators = st.sidebar.multiselect(
        "Select Indicators:",
        options=all_indicators,
        default=list(all_indicators)[:5]
    )

    year_range = st.sidebar.slider(
        "Select Year Range:",
        int(df['Year'].min()), int(df['Year'].max()), (2000, 2023)
    )

    filtered_df = df[
        (df['Indicator'].isin(selected_indicators)) &
        (df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])
    ]

    tab1, tab2, tab3 = st.tabs(["📈 Line Charts", "📊 Comparative Analysis", "🔍 Indicators Deep Dive"])

    # --- Tab 1: Line Charts ---
    with tab1:
        st.subheader("📈 Trend Analysis")
        for indicator in selected_indicators:
            chart_df = filtered_df[filtered_df['Indicator'] == indicator]
            fig = px.line(
                chart_df, x='Year', y='Value',
                title=f"{indicator} Over Time", markers=True,
                line_shape='linear'
            )
            fig.update_traces(line=dict(color=COLOR_PRIMARY), marker=dict(color=COLOR_SECONDARY))
            fig.update_layout(hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)

    # --- Tab 2: Comparative Analysis ---
    with tab2:
        st.subheader("📊 Compare Selected Indicators")
        if len(selected_indicators) >= 2:
            fig = make_subplots(
                rows=len(selected_indicators), cols=1,
                shared_xaxes=True,
                subplot_titles=selected_indicators,
                vertical_spacing=0.05
            )
            for i, indicator in enumerate(selected_indicators, start=1):
                chart_df = filtered_df[filtered_df['Indicator'] == indicator]
                fig.add_trace(
                    go.Scatter(
                        x=chart_df['Year'], y=chart_df['Value'],
                        mode='lines+markers',
                        marker=dict(color=COLOR_SECONDARY),
                        line=dict(color=COLOR_PRIMARY),
                        name=indicator
                    ),
                    row=i, col=1
                )
            fig.update_layout(height=300 * len(selected_indicators), hovermode='x unified', showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ Please select at least two indicators for comparison.")

    # --- Tab 3: Deep Dive ---
    with tab3:
        st.subheader("🔍 Multiple Indicators Overview")
        if not filtered_df.empty:
            fig = px.line(
                filtered_df,
                x="Year", y="Value",
                color="Indicator", markers=True,
                color_discrete_sequence=[COLOR_PRIMARY, COLOR_SECONDARY, COLOR_POSITIVE, COLOR_WARNING, COLOR_NEGATIVE],
                title="Selected Indicators Over Time"
            )
            fig.update_layout(hovermode='x unified')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ No data available for the selected filters.")

    # --- KPIs ---
    st.markdown("---")
    st.subheader("📌 Key Metrics")
    if not filtered_df.empty:
        latest_year = filtered_df['Year'].max()
        latest_data = filtered_df[filtered_df['Year'] == latest_year]

        cols = st.columns(min(4, len(latest_data)))
        for col, row in zip(cols, latest_data.itertuples()):
            col.markdown(f"""
                <div style='background-color:{COLOR_BG_SECTION}; padding:1rem; border-radius:10px'>
                    <h4 style='color:{COLOR_TEXT}; margin-bottom:0.2rem'>{row.Indicator} ({int(row.Year)})</h4>
                    <h2 style='color:{COLOR_PRIMARY}; margin-top:0rem'>{row.Value:,.2f}</h2>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No KPI data to display.")

    # --- Raw Data Table ---
    st.markdown("---")
    st.subheader("📁 Raw Data Table")
    st.dataframe(filtered_df.sort_values(["Indicator", "Year"]), use_container_width=True)

# --- Advanced Analysis ---
elif page == "Advanced Analysis":
    st.title("📊 Advanced Statistical Analysis")

    # --- Univariate ---
    st.subheader("📌 Univariate Analysis")
    selected_uni = st.multiselect(
        "Select Indicators for Histogram:",
        options=df['Indicator'].unique(),
        default=list(df['Indicator'].unique())[:3]
    )
    for indicator in selected_uni:
        chart_df = df[df['Indicator'] == indicator]
        fig = px.histogram(
            chart_df, x='Value', nbins=30,
            title=f"Distribution: {indicator}",
            color_discrete_sequence=[COLOR_PRIMARY]
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # --- Bivariate ---
    st.subheader("🔗 Bivariate Analysis")
    col1, col2 = st.columns(2)
    with col1:
        x_indicator = st.selectbox("X-axis Indicator:", options=df['Indicator'].unique())
    with col2:
        y_indicator = st.selectbox("Y-axis Indicator:", options=df['Indicator'].unique())

    x_df = df[df['Indicator'] == x_indicator]
    y_df = df[df['Indicator'] == y_indicator]
    merged_df = pd.merge(x_df, y_df, on='Year', suffixes=('_X', '_Y'))

    if not merged_df.empty:
        fig = px.scatter(
            merged_df,
            x='Value_X', y='Value_Y',
            trendline='ols',
            labels={'Value_X': x_indicator, 'Value_Y': y_indicator},
            title=f"{x_indicator} vs {y_indicator}",
            color_discrete_sequence=[COLOR_POSITIVE]
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # --- Multivariate ---
    st.subheader("📌 Correlation Heatmap")
    selected_multi = st.multiselect(
        "Select indicators for correlation matrix:",
        options=df['Indicator'].unique(),
        default=list(df['Indicator'].unique())[:5]
    )
    multi_df = df[df['Indicator'].isin(selected_multi)]
    pivot_df = multi_df.pivot(index='Year', columns='Indicator', values='Value')
    corr = pivot_df.corr()

    if not corr.empty:
        fig = px.imshow(
            corr, text_auto=True,
            color_continuous_scale="RdBu_r",
            title="Correlation Matrix (Multivariate)"
        )
        st.plotly_chart(fig, use_container_width=True)


