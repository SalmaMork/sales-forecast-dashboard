import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Sales Forecast Dashboard", layout="wide")

st.title("📊 Sales Forecast Dashboard")
st.write("Sales analysis and forecasting using the Superstore dataset.")

# Load data
df = pd.read_csv("data/train.csv")

df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    format="mixed",
    dayfirst=True
)

# Region filter
region = st.selectbox("Select Region", ["All"] + sorted(df["Region"].dropna().unique().tolist()))

if region != "All":
    df = df[df["Region"] == region]

df["Month"] = df["Order Date"].dt.to_period("M")

# KPIs
total_revenue = df["Sales"].sum()
top_region = df.groupby("Region")["Sales"].sum().idxmax()
top_category = df.groupby("Category")["Sales"].sum().idxmax()

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Top Region", top_region)
col3.metric("Top Category", top_category)

# Monthly sales aggregation
monthly_sales = df.groupby("Month")["Sales"].sum().reset_index()
monthly_sales["Month"] = monthly_sales["Month"].astype(str)
monthly_sales["Month_num"] = range(len(monthly_sales))

# Convert month to datetime and extract seasonality info
monthly_sales["Month"] = pd.to_datetime(monthly_sales["Month"])
monthly_sales["Month_of_year"] = monthly_sales["Month"].dt.month

# Smoothing
monthly_sales["Smoothed_Sales"] = monthly_sales["Sales"].rolling(window=3).mean()
monthly_sales = monthly_sales.dropna().reset_index(drop=True)

# Seasonality encoding with sin/cos
monthly_sales["Month_sin"] = np.sin(2 * np.pi * monthly_sales["Month_of_year"] / 12)
monthly_sales["Month_cos"] = np.cos(2 * np.pi * monthly_sales["Month_of_year"] / 12)

# Train forecasting model
X = monthly_sales[["Month_num", "Month_sin", "Month_cos"]]
y = monthly_sales["Smoothed_Sales"]

model = LinearRegression()
model.fit(X, y)

# Future forecast
future_months = np.arange(
    monthly_sales["Month_num"].max() + 1,
    monthly_sales["Month_num"].max() + 13
)
future_dates = pd.date_range(
    start=monthly_sales["Month"].max() + pd.offsets.MonthBegin(1),
    periods=12,
    freq="MS"
)
future_df = pd.DataFrame({
    "Month_num": future_months,
    "Month": future_dates
})

future_df["Month_of_year"] = future_df["Month"].dt.month
future_df["Month_sin"] = np.sin(2 * np.pi * future_df["Month_of_year"] / 12)
future_df["Month_cos"] = np.cos(2 * np.pi * future_df["Month_of_year"] / 12)

predictions = model.predict(future_df[["Month_num", "Month_sin", "Month_cos"]])

# Charts layout
left, right = st.columns(2)

with left:
    st.subheader("Monthly Sales Trend")
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    ax1.plot(monthly_sales["Month"], monthly_sales["Sales"])
    ax1.set_title("Monthly Sales")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Revenue")
    fig1.autofmt_xdate()
    st.pyplot(fig1)

with right:
    st.subheader("Forecast")
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.plot(monthly_sales["Month_num"], monthly_sales["Sales"], label="Actual Sales", alpha=0.5)
    ax2.plot(monthly_sales["Month_num"], monthly_sales["Smoothed_Sales"], label="Smoothed Sales")
    ax2.plot(future_df["Month_num"], predictions, label="Forecast", linestyle="dashed")
    ax2.set_title("Sales Forecast")
    ax2.set_xlabel("Time")
    ax2.set_ylabel("Revenue")
    ax2.legend()
    st.pyplot(fig2)
