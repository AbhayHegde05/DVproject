import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# --- Page Configuration ---
st.set_page_config(
    page_title="Karnataka Environmental Dashboard",
    page_icon="🌿",
    layout="wide"
)

# --- API Configuration ---
API = "http://localhost:8000"

# --- Helper Functions ---
@st.cache_data
def fetch_data(endpoint):
    try:
        res = requests.get(f"{API}{endpoint}")
        res.raise_for_status()
        return res.json()
    except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
        return None

def post_data(endpoint, payload):
    try:
        res = requests.post(f"{API}{endpoint}", json=payload)
        res.raise_for_status()
        return res.json()
    except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError) as e:
        st.error(f"Could not connect to the backend: {e}. Please ensure the server is running.")
        return None

# --- UI Sidebar ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Logo_of_Karnataka.svg/1200px-Logo_of_Karnataka.svg.png", width=100)
    st.title("Karnataka Dashboard")
    st.info("Select filters here, then use the buttons on the main page to generate analyses.")

districts_list = fetch_data("/insights/districts")
crops_list = fetch_data("/insights/crops")
years_list = list(range(2015, 2026))

if not districts_list or not crops_list:
    st.error("Fatal: Could not fetch initial data from the backend. Please ensure the backend server is running and accessible.")
    st.stop()

# --- Main Page with Tabs ---
st.title("🌿 Karnataka Environmental & Agricultural Dashboard")

tab1, tab2 = st.tabs(["📊 Crop Production Analysis", "🌍 Environmental Impact Analysis"])

# --- Tab 1: Crop Production Analysis ---
with tab1:
    st.header("Analyze Crop Yields Across Districts and Years")
    
    with st.container(border=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            # --- THIS IS THE CORRECTED LINE ---
            selected_districts = st.multiselect("Select Districts", districts_list, default=[districts_list[0]])
        with c2:
            selected_crops = st.multiselect("Select Crops", crops_list, default=[crops_list[0]])
        with c3:
            selected_years = st.multiselect("Select Years", years_list, default=[years_list[-1]])

        if st.button("Generate Crop Yield Visualization", type="primary", key="crop_vis_btn"):
            if not selected_districts or not selected_crops or not selected_years:
                st.warning("Please select at least one district, crop, and year.")
            else:
                payload = {"districts": selected_districts, "crops": selected_crops, "years": selected_years}
                data = post_data("/insights/crop_visualization", payload)
                
                if data:
                    df = pd.DataFrame(data)
                    st.session_state['crop_data'] = df 

                    if not df.empty:
                        fig = px.bar(df, x="district", y="yield_t_ha", color="crop", barmode="group", facet_col="year", title="Crop Yield (tons/ha) Comparison")
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No data available for the selected filters.")
    
    if 'crop_data' in st.session_state and not st.session_state['crop_data'].empty:
        with st.container(border=True):
            st.header("🤖 AI Data Assistant")
            st.info("Ask a question about the data shown in the chart above.", icon="💡")
            user_query = st.text_input("Your Question:", placeholder="e.g., Which district had the highest yield for Sugarcane in 2023?")
            
            if st.button("Ask AI", key="ai_btn"):
                if user_query:
                    chat_payload = {"query": user_query, "data": st.session_state['crop_data'].to_dict(orient="records")}
                    with st.spinner("The AI is analyzing the data..."):
                        response = post_data("/chat/", chat_payload)
                        if response and "response" in response:
                            st.markdown(response["response"])
                        elif response and "error" in response:
                            st.error(f"AI Error: {response['error']}. Is your Gemini API key set correctly?")

# --- Tab 2: Environmental Impact Analysis ---
with tab2:
    st.header("Explore the Relationship Between Yields and Environment")
    
    with st.container(border=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            env_district = st.selectbox("Select a District", districts_list, key="env_dist")
        with c2:
            env_crop = st.selectbox("Select a Crop", crops_list, key="env_crop")
        with c3:
            env_factor = st.selectbox("Select Environmental Factor", ["Rainfall", "Average Temperature"], key="env_factor")

        if st.button("Analyze Environmental Impact", type="primary", key="env_btn"):
            if env_district and env_crop and env_factor:
                factor_map = {"Rainfall": "total_rainfall_mm", "Average Temperature": "avg_temp_c"}
                payload = {"district": env_district, "crop": env_crop}
                corr_data = post_data("/insights/environmental_correlation", payload)

                if corr_data:
                    df_corr = pd.DataFrame(corr_data)
                    if not df_corr.empty and df_corr.shape[0] > 1:
                        fig_corr = px.scatter(
                            df_corr, x=factor_map[env_factor], y="yield_t_ha",
                            trendline="ols", title=f"Yield of {env_crop} vs. {env_factor} in {env_district}"
                        )
                        st.plotly_chart(fig_corr, use_container_width=True)
                    else:
                        st.info("Not enough data points to create a correlation plot for these options.")