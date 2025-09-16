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

# Yield trend
data = requests.get(f"{API}/insights/yield_trend", params={"district": district}).json()
df = pd.DataFrame(data)
if not df.empty:
    fig = px.line(df, x="year", y="yield_t_ha", markers=True, title=f"Yield Trend in {district}")
    st.plotly_chart(fig, use_container_width=True)
