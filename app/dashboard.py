# =========================================================
# 🚀 CYBER CRIME AI DASHBOARD (PRO MAX VERSION)
# =========================================================
# Enhancements:
# ✔ API integration (AI + Alerts + Hotspots)
# ✔ Local fallback (if API fails)
# ✔ Debug logs in terminal
# ✔ Self-healing data + API calls
# ✔ Structured modular functions
# ✔ No breaking changes to your original logic
# =========================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
import sys
import traceback
import requests
from datetime import datetime
from streamlit_lottie import st_lottie

# ================================
# 🔧 PATH FIX
# ================================
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils import get_state_info, generate_ai_explanation, get_crime_legal_info

# ================================
# ⚙️ CONFIG
# ================================
st.set_page_config(page_title="Cyber Crime AI Dashboard", layout="wide")

DATA_PATH = "data/processed/final_dataset.csv"
PRED_PATH = "data/processed/future_predictions.csv"
GEO_PATH = "data/india_states_new.geojson"

# 🔥 API CONFIG
API_URL = "http://127.0.0.1:8000"

# ================================
# 🧠 DEBUG LOGGER & UTILS
# ================================
def log(msg):
    print(f"[DASHBOARD] {msg}")

@st.cache_data
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Load cyber lottie animation
cyber_lottie = load_lottieurl("https://lottie.host/936e0dcf-8bb6-46b0-bcd3-6ee6805b4b74/4BwZZ5x25O.json")

# ================================
# 🔌 API CONNECTORS (WITH FALLBACK)
# ================================
def safe_api_call(endpoint, params=None, fallback=None):
    try:
        url = f"{API_URL}{endpoint}"
        log(f"Calling API → {url}")
        res = requests.get(url, params=params, timeout=5)

        if res.status_code == 200:
            return res.json()
        else:
            log(f"API error {res.status_code}")

    except Exception as e:
        log(f"API FAILED → {e}")

    # fallback
    if fallback:
        log("Using fallback function")
        return fallback()

    return None


def get_ai_analysis_api(state, crime, fallback_data):
    response = safe_api_call(
        "/analysis",
        params={"state": state, "crime": crime}
    )

    if response and "analysis" in response:
        return response["analysis"]

    # fallback → local AI
    return generate_ai_explanation(fallback_data)


def get_alerts_api():
    response = safe_api_call("/alerts")
    if response and "alerts" in response:
        return response["alerts"]
    from src.ai_engine import generate_alerts
    return generate_alerts(df)


def get_hotspots_api():
    response = safe_api_call("/hotspots")
    if response and "data" in response:
        return pd.DataFrame(response["data"])
    from src.ai_engine import get_hotspots
    return get_hotspots(pred_df)

# ================================
# 🗺️ STATE MAP FIX
# ================================
STATE_MAP = {
    "ANDAMAN AND NICOBAR ISLANDS": "Andaman and Nicobar",
    "ANDHRA PRADESH": "Andhra Pradesh",
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
    "ODISHA": "Orissa",
    "PUNJAB": "Punjab",
    "RAJASTHAN": "Rajasthan",
    "SIKKIM": "Sikkim",
    "TAMIL NADU": "Tamil Nadu",
    "TELANGANA": "Andhra Pradesh",
    "TRIPURA": "Tripura",
    "UTTAR PRADESH": "Uttar Pradesh",
    "UTTARAKHAND": "Uttaranchal",
    "WEST BENGAL": "West Bengal",
    "DELHI": "Delhi",
    "JAMMU AND KASHMIR": "Jammu and Kashmir",
    "LADAKH": "Jammu and Kashmir",
    "LAKSHADWEEP": "Lakshadweep",
    "PUDUCHERRY": "Puducherry",
    "CHANDIGARH": "Chandigarh",
    "DAMAN AND DIU": "Daman and Diu",
    "DADRA AND NAGAR HAVELI": "Dadra and Nagar Haveli"
}

# ================================
# 📊 LOAD DATA (SAFE)
# ================================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv(DATA_PATH)
        pred = pd.read_csv(PRED_PATH)

        log(f"Dataset loaded → {df.shape}")
        return df, pred

    except Exception as e:
        st.error(f"[ERROR] Data loading failed: {e}")
        print(traceback.format_exc())
        return pd.DataFrame(), pd.DataFrame()

df, pred_df = load_data()

# ================================
# 🗺️ LOAD GEOJSON
# ================================
geojson = None
try:
    if os.path.exists(GEO_PATH):
        with open(GEO_PATH) as f:
            geojson = json.load(f)
            log("GeoJSON loaded")
except Exception as e:
    log(f"GeoJSON error: {e}")

# ================================
# 🎯 TITLE & ANIMATION
# ================================
colA, colB = st.columns([1, 4])
with colA:
    if cyber_lottie:
        st_lottie(cyber_lottie, height=120, key="header_anim")
with colB:
    st.title("🚨 Cyber Crime AI Intelligence Dashboard")
    st.markdown("""
    **Created by Himanshu Yadav**  
    B.Tech-M.Tech CSE (Cybersecurity) | National Forensic Science University (NFSU), Tripura Campus  
    👉 *Self-learned AI/ML Project - Pro Max Evolution*
    """)

# ================================
# SIDEBAR
# ================================
mode = st.sidebar.radio(
    "Select View",
    ["Overview", "State Analysis", "Crime Analysis", "Compare States", "Cyber Laws & Agencies"]
)

# ================================
# 🚨 ALERT SYSTEM (GLOBAL)
# ================================
st.sidebar.subheader("🚨 Live Alerts")

alerts = get_alerts_api()

if alerts:
    for a in alerts[:5]:
        st.sidebar.warning(a)
else:
    st.sidebar.success("No major alerts")

# ================================
# RISK FUNCTION
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

    st.subheader("🚨 Live Cyber Crime Alerts")
    if alerts:
        for a in alerts[:3]:
            st.error(a)
    else:
        st.success("No active major cyber threats detected.")

    st.markdown("---")
    st.subheader("🗺️ India Crime Heatmap")

    map_data = df.copy()
    map_data["geo_state"] = map_data["state"].map(STATE_MAP)
    map_data = map_data.dropna(subset=["geo_state"])
    map_agg = map_data.groupby("geo_state")["cases"].sum().reset_index()

    if geojson:
        fig = px.choropleth(
            map_agg,
            geojson=geojson,
            locations="geo_state",
            featureidkey="properties.NAME_1",
            color="cases",
            hover_name="geo_state",
            color_continuous_scale="RdBu_r",
            template="plotly_dark"
        )
        fig.update_geos(fitbounds="locations", visible=False, bgcolor="rgba(0,0,0,0)")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    # 🔥 HOTSPOTS FROM API
    st.subheader("🔥 Top 5 Dangerous States (Predicted)")

    hotspots = get_hotspots_api()

    if not hotspots.empty:
        st.dataframe(hotspots, use_container_width=True)
        fig2 = px.bar(hotspots, x="state", y="predicted_cases", color="predicted_cases", color_continuous_scale="Reds", template="plotly_dark")
        fig2.update_traces(marker_line_width=1.5, opacity=0.8)
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig2, use_container_width=True)

# ================================
# 🏙️ STATE ANALYSIS
# ================================
elif mode == "State Analysis":

    state = st.selectbox("Select State", sorted(df["state"].unique()))
    state_data = df[df["state"] == state]
    info = get_state_info(state)

    st.subheader(f"📍 {state}")

    st.write(f"""
**Capital:** {info.get("capital", "N/A")}  
**CM:** {info.get("cm", "N/A")}  
**Governor:** {info.get("governor", "N/A")}  
**Formation:** {info.get("formation", "N/A")}  
**Region:** {info.get("region", "N/A")}  
**IT Literacy Index:** {info.get("it_literacy_index", "N/A")}  
**Cyber Nodal Agency:** {info.get("cyber_nodal_agency", "N/A")}  
**National Helpline:** {info.get("helpline", "1930")}  
""")

    total_cases = state_data["cases"].sum()
    st.metric("🚨 Risk Level", get_risk_level(total_cases))

    # ⚖️ LEGAL INFO
    st.subheader("⚖️ Legal Provisions")
    crime = state_data["category"].iloc[0]
    legal_info = get_crime_legal_info(crime)
    col1, col2, col3 = st.columns(3)
    col1.metric("BNS Section", legal_info["BNS"])
    col2.metric("IPC Section", legal_info["IPC"])
    col3.metric("IT Act", legal_info["IT_Act"])
    st.write(f"**Punishment:** {legal_info['Punishment']} | **Fine:** {legal_info['Fine']}")

    # 🤖 AI (API + fallback)
    st.subheader("🤖 AI Insight")
    analysis = get_ai_analysis_api(state, crime, state_data)
    st.info(analysis)

    fig = px.line(state_data, x="year", y="cases", color="category", markers=True, template="plotly_dark")
    fig.update_traces(line_shape="spline", line=dict(width=3), marker=dict(size=8, symbol="hexagram"))
    fig.update_layout(hovermode="x unified", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", transition_duration=500)
    st.plotly_chart(fig, use_container_width=True)

# ================================
# 🔍 CRIME ANALYSIS
# ================================
elif mode == "Crime Analysis":

    crime = st.selectbox("Select Crime", sorted(df["category"].unique()))
    crime_data = df[df["category"] == crime]

    st.subheader(f"⚖️ Crime: {crime}")

    # ⚖️ LEGAL INFO
    legal_info = get_crime_legal_info(crime)
    st.markdown("### 📜 Indian Laws & Penalties")
    cols = st.columns(3)
    cols[0].metric("BNS Section", legal_info["BNS"])
    cols[1].metric("IPC Section", legal_info["IPC"])
    cols[2].metric("IT Act", legal_info["IT_Act"])
    st.write(f"**Punishment:** {legal_info['Punishment']} &nbsp; | &nbsp; **Fine:** {legal_info['Fine']}")

    st.subheader("🤖 AI Insight")
    analysis = get_ai_analysis_api("India", crime, crime_data)
    st.info(analysis)

    fig = px.bar(crime_data, x="state", y="cases", color="cases", color_continuous_scale="Plasma", template="plotly_dark")
    fig.update_traces(marker_line_width=1.5, opacity=0.9)
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", xaxis={'categoryorder':'total descending'})
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

    fig = px.line(combined, x="year", y="cases", color="state", markers=True, template="plotly_dark")
    fig.update_traces(line_shape="spline", line=dict(width=4), marker=dict(size=10))
    fig.update_layout(hovermode="x unified", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", transition_duration=500)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🤖 AI Comparison Insight")

    analysis = get_ai_analysis_api(f"{state1} vs {state2}", "comparison", combined)
    st.info(analysis)

# ================================
# 📚 CYBER LAWS & AGENCIES
# ================================
elif mode == "Cyber Laws & Agencies":

    st.subheader("🏛️ Indian Cyber Laws, Definitions & Govt Agencies")
    from src.utils import CRIME_LEGAL_INFO
    
    tabs = st.tabs(["📖 Cyber Crime Dictionary", "🏢 Government Agencies", "⚖️ BNS & IPC Mappings"])
    
    with tabs[0]:
        st.markdown("### Crime Dictionary & Legal Provisions")
        for crime, details in CRIME_LEGAL_INFO.items():
            with st.expander(f"📌 {crime.title()}"):
                st.write(f"**BNS Section:** {details['BNS']}")
                st.write(f"**IPC Section:** {details['IPC']}")
                st.write(f"**IT Act:** {details['IT_Act']}")
                st.write(f"**Punishment:** {details['Punishment']}")
                st.write(f"**Fine:** {details['Fine']}")
                st.info("Navigate to `Crime Analysis` for dynamic AI Motive & Prevention breakdown.")
    
    with tabs[1]:
        st.markdown("### 🏢 Government Bodies for Solving Cyber Crime")
        st.markdown('''
        * **I4C (Indian Cyber Crime Coordination Centre):** An initiative of the Ministry of Home Affairs to deal with cyber crime in a coordinated and comprehensive manner. Nodal reporting portal: [cybercrime.gov.in](https://cybercrime.gov.in)
        * **CERT-In (Computer Emergency Response Team - India):** Nodal agency to deal with cyber security threats like hacking, malware outbreaks, and phishing.
        * **NCIIPC (National Critical Information Infrastructure Protection Centre):** Protects critical information infrastructure in India (Banking, Power, Defence grids).
        * **CVP (Cyber Volunteer Program):** Citizen outreach program to report unlawful and malicious online content.
        * **State Cyber Cells / Cyber Police Stations:** Every police department in Indian states has a dedicated cyber cell acting as the first line of intervention for citizens.
        ''')
        
    with tabs[2]:
        st.markdown("### ⚖️ Bharatiya Nyaya Sanhita (BNS) vs IPC")
        st.markdown('''
        The **Bharatiya Nyaya Sanhita (BNS)** has replaced the Indian Penal Code (IPC) as the primary criminal code. Important mappings for cyber-offenses:
        
        * **Theft/Data Theft:** BNS Sec 303 (Old IPC 378)
        * **Extortion:** BNS Sec 308 (Old IPC 383, 384)
        * **Cheating/Cyber Fraud:** BNS Sec 318 (Old IPC 415, 420)
        * **Defamation/Bullying:** BNS Sec 356 (Old IPC 499)
        * **Rape/Cyber Sexual Exploitation:** BNS Sec 64 (Old IPC 376)
        
        *Note: IT Act (Information Technology Act, 2000) overrides general laws for specific cyber provisions.*
        ''')