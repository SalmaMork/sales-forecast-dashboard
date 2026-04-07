# 📊 Sales Forecast Dashboard

This project analyzes sales data from the Superstore dataset and builds a forecasting model to predict future revenue.  
It also includes an interactive dashboard built with Streamlit to visualize key insights.

---

## 🚀 Features

- 📈 Total Revenue KPI
- 🌍 Top Region identification
- 🛍️ Top Category analysis
- 📊 Monthly Sales Trend visualization
- 🔮 Sales Forecast using Linear Regression
- 🔁 Seasonality modeling using sine and cosine encoding
- 🎛️ Interactive Region filter (Streamlit dashboard)

---

## 🖼️ Dashboard Preview

![Dashboard Screenshot](screenshots/dashboard.png)

---

## 🧠 Project Overview

### 1. Data Preparation
- Loaded dataset using Pandas
- Converted `Order Date` to datetime format
- Aggregated sales monthly

### 2. KPI Analysis
- Total Revenue
- Top-performing Region
- Top-performing Category

### 3. Trend Analysis
- Monthly sales trends visualized over time

### 4. Forecasting Model
- Linear Regression used to model sales over time
- Applied **moving average smoothing** to reduce noise
- Added **seasonality encoding** using sine and cosine transformations

### 5. Dashboard
- Built using Streamlit
- Displays KPIs, trends, and forecasts
- Includes interactive filtering by region

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- Streamlit

---

## 📁 Project Structure
