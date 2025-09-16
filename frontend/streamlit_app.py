import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API = "http://localhost:8000"

st.set_page_config(page_title="Karnataka Dashboard", layout="wide")
st.title("🌍 Karnataka Environmental Dashboard")

# District selector
districts = requests.get(f"{API}/insights/districts").json()
district = st.selectbox("Select District", districts)

# Create columns for layout
col1, col2 = st.columns(2)

with col1:
    # Yield trend
    st.subheader(f"Yield Trend in {district}")
    data = requests.get(f"{API}/insights/yield_trend", params={"district": district}).json()
    df = pd.DataFrame(data)
    if not df.empty:
        fig = px.line(df, x="year", y="yield_t_ha", markers=True, title=f"Overall Yield Trend in {district}")
        st.plotly_chart(fig, use_container_width=True)

    # Crop specific yield trend
    st.subheader(f"Crop-Specific Yield Trend in {district}")
    crops = requests.get(f"{API}/insights/crops", params={"district": district}).json()
    crop = st.selectbox("Select Crop", ["All"] + crops)

    if crop != "All":
        data = requests.get(f"{API}/insights/yield_trend", params={"district": district, "crop": crop}).json()
        df = pd.DataFrame(data)
        if not df.empty:
            fig = px.line(df, x="year", y="yield_t_ha", markers=True, title=f"Yield Trend for {crop} in {district}")
            st.plotly_chart(fig, use_container_width=True)

with col2:
    # Rainfall
    st.subheader(f"Monthly Rainfall in {district}")
    data = requests.get(f"{API}/insights/rainfall", params={"district": district}).json()
    df = pd.DataFrame(data)
    if not df.empty:
        df["month"] = pd.to_datetime(df["month"], format="%m").dt.strftime("%B")
        fig = px.bar(df, x="month", y="rainfall_mm", color="year", barmode="group", title=f"Monthly Rainfall in {district}")
        st.plotly_chart(fig, use_container_width=True)

    # Air Quality
    st.subheader(f"Air Quality Trend in {district}")
    data = requests.get(f"{API}/insights/air_quality", params={"district": district}).json()
    df = pd.DataFrame(data)
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])
        fig = px.line(df, x="date", y=["pm25", "pm10", "aqi"], markers=True, title=f"Air Quality Trend in {district}")
        st.plotly_chart(fig, use_container_width=True)