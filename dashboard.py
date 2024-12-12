import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import Pipeline


# Load Data
data = pd.read_csv("advertising_sales.csv")


# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page", ["Overview", "Ad Performance", "Predict Sales", "Download Reports"])

# 1. Overview
if page == "Overview":
    st.title("Ad Performance Analytics Dashboard")
    st.subheader("Dataset Summary")
    st.write(data.head())

    # Key statistics
    st.subheader("Key Statistics")
    st.write(data.describe())

    # KPIs
    total_spend = data[['TV Ad Budget ($)', 'Radio Ad Budget ($)', 'Newspaper Ad Budget ($)']].sum().sum()
    avg_sales = data['Sales ($)'].mean()
    correlation = data.corr()['Sales ($)'][1:]

    st.metric("Total Ad Spend (Millions)", f"${total_spend / 1000:.2f}")
    st.metric("Average Sales (Millions)", f"${avg_sales:.2f}")
    st.write("Ad Effectiveness (Correlation with Sales):")
    st.bar_chart(correlation)

# 2. Ad Performance
elif page == "Ad Performance":
    st.title("Ad Performance Insights")

    # Ad spending vs sales
    st.subheader("Ad Spending vs Sales")
    for ad_type in ['TV Ad Budget ($)', 'Radio Ad Budget ($)', 'Newspaper Ad Budget ($)']:
        st.write(f"**{ad_type} vs Sales**")
        plt.figure(figsize=(8, 4))
        sns.scatterplot(x=data[ad_type], y=data['Sales ($)'])
        plt.title(f"{ad_type} vs Sales")
        plt.xlabel(f"{ad_type} (Thousands)")
        plt.ylabel("Sales (Millions)")
        st.pyplot(plt)

    # Interaction Effects
    st.subheader("Interaction Effects")
    sns.heatmap(data.corr(), annot=True, cmap='coolwarm')
    st.pyplot(plt)

# 3. Predict Sales
elif page == "Predict Sales":
    st.title("Predict Sales")

    # User inputs
    st.subheader("Input Ad Budgets (in Thousands)")
    tv_budget = st.number_input("TV Budget ($)", min_value=0.0, max_value=500.0, value=50.0)
    radio_budget = st.number_input("Radio Budget ($)", min_value=0.0, max_value=500.0, value=25.0)
    newspaper_budget = st.number_input("Newspaper Budget ($)", min_value=0.0, max_value=500.0, value=15.0)

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
    st.write(f"Predicted Sales: ${predicted_sales:.2f} Million")

    # Visualization
    st.bar_chart({"Ad Budgets": [tv_budget, radio_budget, newspaper_budget], "Predicted Sales": [predicted_sales]})

# 4. Download Reports
elif page == "Download Reports":
    st.title("Download Reports")
    st.download_button("Download Dataset", data.to_csv(), file_name="ad_performance.csv", mime="text/csv")
