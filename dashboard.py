import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_echarts import st_echarts

# Load Data
data = pd.read_csv("advertising_sales.csv")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page", ["Overview", "Ad Performance", "Predict Sales", "Report"])

# KPIs
with st.sidebar:
    total_spend = data[['TV Ad Budget ($)',
                        'Radio Ad Budget ($)', 'Newspaper Ad Budget ($)']].sum().sum() * 1000
    avg_total_spend = data[['TV Ad Budget ($)',
                            'Radio Ad Budget ($)', 'Newspaper Ad Budget ($)']].sum(axis=1).mean() * 1000
    avg_sales = data['Sales ($)'].mean() * 1000000
    total_sale = data['Sales ($)'].sum() * 1000000
    average_roi = (avg_sales - avg_total_spend) / avg_total_spend
    correlation = data.corr()['Sales ($)'][1:]
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.metric("Total Ad Spend", f"${total_spend:,.2f}")
    st.divider()
    st.metric("Average Ad Spend", f"${avg_total_spend:,.2f}")
    st.divider()
    st.metric("Total Sales", f"${total_sale:,.2f}")
    st.divider()
    st.metric("Average Sales", f"${avg_sales:,.2f}")
    st.divider()
    st.metric("Average ROI", f"{average_roi * 100:,.2f}%")

# Overview Page
if page == "Overview":
    st.title("Ad Performance Analytics Dashboard")
    st.divider()
    st.markdown("<br>", unsafe_allow_html=True)
    # Key statistics
    stats = data.describe().drop(columns=["ID"])
    st.subheader("Key Statistics")
    st.divider()
    st.markdown("<br>", unsafe_allow_html=True)
    st.write(stats)
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.write("Ad Effectiveness (Correlation with Sales):")
    st.divider()
    st.markdown("<br>", unsafe_allow_html=True)
    st.bar_chart(correlation.drop('Sales ($)'))

# 2. Ad Performance
elif page == "Ad Performance":
    st.title("Ad Performance Insights")

    # Ad spending vs sales
    for ad_type in ['TV Ad Budget ($)', 'Radio Ad Budget ($)', 'Newspaper Ad Budget ($)']:
        st.write(f"**{ad_type} vs Sales**")

        # Prepare data for scatter plot
        scatter_data = [[x, y] for x, y in zip(data[ad_type], data["Sales ($)"])]  # Fixed format

        # ECharts options for scatter plot
        options = {
            "tooltip": {
                "trigger": "item",
                "formatter": "Ad Spend: {c[0]:,.2f}<br>Sales: {c[1]:,.2f}",
            },
            "xAxis": {
                "type": "value",
                "name": f"{ad_type} (Thousands)",
                "nameLocation": "middle",
                "nameGap": 30,
            },
            "yAxis": {
                "type": "value",
                "name": "Sales (Millions)",
                "nameLocation": "middle",
                "nameGap": 40,
            },
            "series": [
                {
                    "name": f"{ad_type} vs Sales",
                    "type": "scatter",
                    "data": scatter_data,
                    "symbolSize": 8,  # Adjust size of points
                    "itemStyle": {"color": "#1f77b4"},  # Customize point color
                }
            ],
            "title": {
                "text": f"{ad_type} vs Sales",
                "left": "center",
                "top": "5%",
            },
        }

        # Render scatter plot
        st_echarts(options=options, height="400px")


# 3. Predict Sales
elif page == "Predict Sales":
    st.title("Predict Sales")

    # User inputs
    st.subheader("Input Ad Budgets")

    # TV Budget Slider
    tv_full = st.slider(
        "TV Budget ($)",
        min_value=0.0,
        max_value=250000.0,
        value=50000.0,
        step=1000.0,  # Set the step size
    )
    tv_budget = tv_full / 1000000  # Convert to millions

    # Radio Budget Slider
    radio_full = st.slider(
        "Radio Budget ($)",
        min_value=0.0,
        max_value=100000.0,
        value=25000.0,
        step=1000.0,  # Set the step size
    )
    radio_budget = radio_full / 1000000  # Convert to millions

    # Newspaper Budget Slider
    newspaper_full = st.slider(
        "Newspaper Budget ($)",
        min_value=0.0,
        max_value=100000.0,
        value=15000.0,
        step=1000.0,  # Set the step size
    )
    newspaper_budget = newspaper_full / 1000000  # Convert to millions

    # Predictive model
    st.subheader("Predicted Sales (Millions)")
    model_coefficients = {
        "const": 6.3249,
        "Log_TV_Budget": 23.1818,
        "Log_Radio_Budget": 16.0265,
        "Log_Newspaper_Budget": 15.5851,
        "Log_TV_Radio_Interaction": 1321.7793,
        "Log_TV_Newspaper_Interaction": -86.6449,
        "Log_Radio_Newspaper_Interaction": -43.9794
    }

    log_tv = np.log(tv_budget + 1)
    log_radio = np.log(radio_budget + 1)
    log_newspaper = np.log(newspaper_budget + 1)
    log_tv_radio = log_tv * log_radio
    log_tv_newspaper = log_tv * log_newspaper
    log_radio_newspaper = log_radio * log_newspaper

    predicted_sales = (
            model_coefficients["const"] +
            model_coefficients["Log_TV_Budget"] * log_tv +
            model_coefficients["Log_Radio_Budget"] * log_radio +
            model_coefficients["Log_Newspaper_Budget"] * log_newspaper +
            model_coefficients["Log_TV_Radio_Interaction"] * log_tv_radio +
            model_coefficients["Log_TV_Newspaper_Interaction"] * log_tv_newspaper +
            model_coefficients["Log_Radio_Newspaper_Interaction"] * log_radio_newspaper
    )
    st.write(f"Predicted Sales: ${predicted_sales:,.2f} Million")

