
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load dataset
df = pd.read_csv("updated_dataset 1.4.csv", encoding="latin1")

# Streamlit Title
st.title("📊 Amazon Sales Dashboard")

# Sidebar Filters
st.sidebar.header("Filters")
selected_brands = st.sidebar.multiselect("Select Brand", df["Brand"].unique())
selected_asins = st.sidebar.multiselect("Select ASIN", df["ASIN"].unique())

# Data Filtering
filtered_df = df.copy()
if selected_brands:
    filtered_df = filtered_df[filtered_df["Brand"].isin(selected_brands)]
if selected_asins:
    filtered_df = filtered_df[filtered_df["ASIN"].isin(selected_asins)]

# KPI Calculations
if not filtered_df.empty:
    total_sales = filtered_df["based on Avg Sales"].sum()
    total_forecast = filtered_df["based on forecast"].sum()
    avg_7 = filtered_df["avg. Daily sales (7 days)"].sum()
    avg_30 = filtered_df["avg. Daily sales (30 days)"].sum()
    growth_percentage = ((avg_7 - avg_30) / avg_30 * 100) if avg_30 != 0 else 0
    total_stock = filtered_df[["FBA Stock", "3PL Stock"]].sum().sum()
    top_sku = filtered_df.sort_values("based on Avg Sales", ascending=False)["ASIN"].iloc[0]
else:
    total_sales, total_forecast, total_stock, growth_percentage = 0, 0, 0, 0
    top_sku = "No Data"

# Display KPI Cards
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"{total_sales:,}")
col2.metric("Total Forecasted Sales", f"{total_forecast:,}")
col3.metric("7-day vs. 30-day Growth %", f"{growth_percentage:.2f}%")

col4, col5 = st.columns(2)
col4.metric("Total FBA & 3PL Stock", f"{total_stock:,}")
col5.metric("Top Selling SKU", top_sku)

# Bar Chart: Forecast vs. Avg Sales by SKU
if not filtered_df.empty:
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=filtered_df["ASIN"], y=filtered_df["based on forecast"], name="Forecasted Sales"))
    fig_bar.add_trace(go.Bar(x=filtered_df["ASIN"], y=filtered_df["based on Avg Sales"], name="Average Sales"))
    fig_bar.update_layout(title="Forecast vs. Avg Sales by SKU", barmode="group")
else:
    fig_bar = go.Figure().update_layout(title="No Data Available")

st.plotly_chart(fig_bar)

# Speedometer (Gauge) Chart: 7-day vs. 30-day Growth %
if not filtered_df.empty:
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=growth_percentage,
        title={"text": "7-day vs. 30-day Growth %"},
        gauge={"axis": {"range": [-100, 100]}, "bar": {"color": "green"}}
    ))
else:
    fig_gauge = go.Figure().update_layout(title="No Data Available")

st.plotly_chart(fig_gauge)

# Stacked Bar Chart: FBA Stock, 3PL Stock & FBA Pending
if not filtered_df.empty:
    fig_stacked = go.Figure()
    fig_stacked.add_trace(go.Bar(x=filtered_df["ASIN"], y=filtered_df["FBA Stock"], name="FBA Stock"))
    fig_stacked.add_trace(go.Bar(x=filtered_df["ASIN"], y=filtered_df["3PL Stock"], name="3PL Stock"))
    fig_stacked.add_trace(go.Bar(x=filtered_df["ASIN"], y=filtered_df["FBA Pending"], name="FBA Pending"))
    fig_stacked.update_layout(title="FBA Stock, FBA Pending & 3PL Stock by SKU", barmode="stack")
else:
    fig_stacked = go.Figure().update_layout(title="No Data Available")

st.plotly_chart(fig_stacked)

# Joint Bar Chart: Forecast.2 vs. AvgSales.2 by SKU
if not filtered_df.empty:
    fig_joint = go.Figure()
    fig_joint.add_trace(go.Bar(x=filtered_df["ASIN"], y=filtered_df["basedonforecast.2"], name="Forecast.2 Sales"))
    fig_joint.add_trace(go.Bar(x=filtered_df["ASIN"], y=filtered_df["basedonAvgSales.2"], name="AvgSales.2"))
    fig_joint.update_layout(title="Forecast.2 vs. Avg Sales.2 by SKU", barmode="group")
else:
    fig_joint = go.Figure().update_layout(title="No Data Available")

st.plotly_chart(fig_joint)
    