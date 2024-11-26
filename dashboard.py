# dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
data = pd.read_csv("advertising_sales.csv")

# Calculate ROI for each channel
data['TV ROI (%)'] = ((data['Sales ($)'] - data['TV Ad Budget ($)']) / data['TV Ad Budget ($)']) * 100
data['Radio ROI (%)'] = ((data['Sales ($)'] - data['Radio Ad Budget ($)']) / data['Radio Ad Budget ($)']) * 100
data['Newspaper ROI (%)'] = ((data['Sales ($)'] - data['Newspaper Ad Budget ($)']) / data['Newspaper Ad Budget ($)']) * 100

# Streamlit App Layout
st.title("Advertising Sales Dashboard")

# Filter by TV Budget
st.header("Filter by TV Budget")
tv_min = st.slider("Minimum TV Ad Budget", min_value=0, max_value=int(data['TV Ad Budget ($)'].max()), value=50)
filtered_data = data[data['TV Ad Budget ($)'] >= tv_min]
st.write(f"Filtered Data with TV Budget >= {tv_min}")
st.dataframe(filtered_data)

# ROI Visualization
st.header("Return on Investment (ROI) by Channel")
roi_means = {
    'Channel': ['TV', 'Radio', 'Newspaper'],
    'Average ROI (%)': [
        data['TV ROI (%)'].mean(),
        data['Radio ROI (%)'].mean(),
        data['Newspaper ROI (%)'].mean(),
    ]
}
roi_df = pd.DataFrame(roi_means)

fig_roi = px.bar(roi_df, x='Channel', y='Average ROI (%)', title="Average ROI by Channel",
                 color='Channel', text='Average ROI (%)', labels={'Average ROI (%)': 'ROI (%)'})
fig_roi.update_traces(texttemplate='%{text:.2f}', textposition='outside')
fig_roi.update_layout(yaxis_title="ROI (%)", xaxis_title="Channel")
st.plotly_chart(fig_roi)

# Pie Chart for Ad Budget Allocation
st.header("Ad Budget Allocation by Channel")
total_budget = {
    'Channel': ['TV', 'Radio', 'Newspaper'],
    'Total Spend ($)': [
        data['TV Ad Budget ($)'].sum(),
        data['Radio Ad Budget ($)'].sum(),
        data['Newspaper Ad Budget ($)'].sum(),
    ]
}
budget_df = pd.DataFrame(total_budget)

# Plotly Pie Chart
fig_pie = px.pie(budget_df, values='Total Spend ($)', names='Channel',
                 title="Ad Budget Allocation by Channel", hole=0.4)
fig_pie.update_traces(textinfo='percent+label')
st.plotly_chart(fig_pie)
