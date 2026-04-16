import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
import sys

# ================================
# PATH FIX (IMPORTANT)
# This ensures Python can access src/utils.py
# ================================
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils import get_state_info, generate_ai_explanation

# ================================
# CONFIG
# ================================
st.set_page_config(page_title="Cyber Crime AI Dashboard", layout="wide")

DATA_PATH = "data/processed/final_dataset.csv"
PRED_PATH = "data/processed/future_predictions.csv"
GEO_PATH = "data/india_states.geojson"

# ================================
# STATE NAME MAPPING (CRITICAL FIX)
# This maps your dataset states → GeoJSON states
# Without this → map will NOT render
# ================================
STATE_MAP = {
    "ANDAMAN AND NICOBAR ISLANDS": "Andaman & Nicobar",
    "ARUNACHAL PRADESH": "Arunachal Pradesh",
    "ASSAM": "Assam",
    "BIHAR": "Bihar",
    "CHHATTISGARH": "Chhattisgarh",
    "GOA": "Goa",
    "GUJARAT": "Gujarat",
    "HARYANA": "Haryana",
    "HIMACHAL PRADESH": "Himachal Pradesh",
    "JHARKHAND": "Jharkhand",
    "KARNATAKA": "Karnataka",
    "KERALA": "Kerala",
    "MADHYA PRADESH": "Madhya Pradesh",
    "MAHARASHTRA": "Maharashtra",
    "MANIPUR": "Manipur",
    "MEGHALAYA": "Meghalaya",
    "MIZORAM": "Mizoram",
    "NAGALAND": "Nagaland",
    "ODISHA": "Odisha",
    "PUNJAB": "Punjab",
    "RAJASTHAN": "Rajasthan",
    "SIKKIM": "Sikkim",
    "TAMIL NADU": "Tamil Nadu",
    "TELANGANA": "Telangana",
    "TRIPURA": "Tripura",
    "UTTAR PRADESH": "Uttar Pradesh",
    "UTTARAKHAND": "Uttarakhand",
    "WEST BENGAL": "West Bengal",
    "DELHI": "Delhi",
    "JAMMU AND KASHMIR": "Jammu & Kashmir",
    "LADAKH": "Ladakh",
    "LAKSHADWEEP": "Lakshadweep",
    "PUDUCHERRY": "Puducherry",
    "CHANDIGARH": "Chandigarh",
    "DAMAN AND DIU": "Daman & Diu",
    "DADRA AND NAGAR HAVELI": "Dadra & Nagar Haveli"
}

# ================================
# LOAD DATA
# ================================
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    pred = pd.read_csv(PRED_PATH)
    return df, pred

try:
    df, pred_df = load_data()
except Exception as e:
    st.error(f"[ERROR] Data loading failed: {e}")
    st.stop()

# ================================
# LOAD GEOJSON (MAP FILE)
# ================================
geojson = None
if os.path.exists(GEO_PATH):
    with open(GEO_PATH) as f:
        geojson = json.load(f)

# ================================
# TITLE
# ================================
st.title("🚨 Cyber Crime AI Intelligence Dashboard")

st.markdown("""
**Created by Himanshu Yadav**  
B.Tech-M.Tech CSE (Cybersecurity)  
National Forensic Science University (NFSU), Tripura Campus  

👉 Self-learned AI/ML Project
""")

# ================================
# SIDEBAR
# ================================
mode = st.sidebar.radio(
    "Select View",
    ["Overview", "State Analysis", "Crime Analysis", "Compare States"]
)

# ================================
# RISK SCORING FUNCTION
# ================================
def get_risk_level(value):
    if value < 50:
        return "LOW 🟢"
    elif value < 200:
        return "MEDIUM 🟡"
    else:
        return "HIGH 🔴"

# ================================
# 🗺️ OVERVIEW
# ================================
if mode == "Overview":

    st.subheader("🗺️ India Crime Heatmap")

    # Aggregate total crime per state
    map_data = df.groupby("state")["cases"].sum().reset_index()

    # 🔥 MAP FIX: convert dataset names → geojson names
    map_data["geo_state"] = map_data["state"].map(STATE_MAP)

    # Remove states not matching GeoJSON
    map_data = map_data.dropna(subset=["geo_state"])

    # ================================
    # DRAW MAP
    # ================================
    if geojson:
        fig = px.choropleth(
            map_data,
            geojson=geojson,
            locations="geo_state",  # 🔥 KEY FIX
            featureidkey="properties.ST_NM",
            color="cases",
            hover_name="state",     # show original state
            color_continuous_scale="Reds"
        )

        # Fit India map properly
        fig.update_geos(fitbounds="locations", visible=False)

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠ GeoJSON file not found")

    # ================================
    # 🔥 TOP 5 STATES
    # ================================
    st.subheader("🔥 Top 5 High Risk States")

    top_states = map_data.sort_values("cases", ascending=False).head(5)

    for _, row in top_states.iterrows():
        risk = get_risk_level(row["cases"])
        st.write(f"👉 {row['state']} → {int(row['cases'])} cases → {risk}")

# ================================
# 🏙️ STATE ANALYSIS
# ================================
elif mode == "State Analysis":

    state = st.selectbox("Select State", sorted(df["state"].unique()))

    state_data = df[df["state"] == state]
    info = get_state_info(state)

    st.subheader(f"📍 {state}")

    st.write(f"""
Capital: {info.get("capital", "N/A")}  
CM: {info.get("cm", "N/A")}  
Governor: {info.get("governor", "N/A")}  
Formation: {info.get("formation", "N/A")}  
Region: {info.get("region", "N/A")}
""")

    # Risk
    total_cases = state_data["cases"].sum()
    st.metric("🚨 Risk Level", get_risk_level(total_cases))

    # AI Insight
    st.subheader("🤖 AI Insight")
    st.info(generate_ai_explanation(state_data))

    # Graph
    fig = px.line(state_data, x="year", y="cases", color="category")
    st.plotly_chart(fig, use_container_width=True)

# ================================
# 🔍 CRIME ANALYSIS
# ================================
elif mode == "Crime Analysis":

    crime = st.selectbox("Select Crime", sorted(df["category"].unique()))

    crime_data = df[df["category"] == crime]

    st.subheader(f"⚖️ Crime: {crime}")

    st.write("Cyber crime affecting digital systems in India.")

    st.subheader("🤖 AI Insight")
    st.info(generate_ai_explanation(crime_data))

    fig = px.bar(crime_data, x="state", y="cases")
    st.plotly_chart(fig, use_container_width=True)

# ================================
# ⚔️ COMPARE STATES
# ================================
elif mode == "Compare States":

    st.subheader("⚔️ State Comparison")

    col1, col2 = st.columns(2)

    state1 = col1.selectbox("State 1", sorted(df["state"].unique()))
    state2 = col2.selectbox("State 2", sorted(df["state"].unique()))

    data1 = df[df["state"] == state1]
    data2 = df[df["state"] == state2]

    combined = pd.concat([data1, data2])

    fig = px.line(combined, x="year", y="cases", color="state")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🤖 AI Comparison Insight")
    st.info(generate_ai_explanation(combined))