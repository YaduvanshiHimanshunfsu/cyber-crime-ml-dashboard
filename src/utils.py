import re
import pandas as pd

# ================================
# 🔥 RISK ENGINE
# ================================
def calculate_risk_score(df):
    total = df["cases"].sum()

    if total < 500:
        return "🟢 LOW RISK"
    elif total < 2000:
        return "🟡 MEDIUM RISK"
    else:
        return "🔴 HIGH RISK"


# ================================
# 🤖 AI EXPLANATION ENGINE
# ================================
def generate_ai_explanation(data, entity="state"):
    try:
        total = data["cases"].sum()
        trend = data.groupby("year")["cases"].sum()

        growth = ((trend.iloc[-1] - trend.iloc[0]) / (trend.iloc[0] + 1)) * 100

        if total > 5000:
            risk = "HIGH"
        elif total > 1000:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        return f"""
🔍 AI Analysis:

• Total cases: {int(total)}
• Growth: {growth:.2f}%
• Risk Level: {risk}

📈 Insight:
The {entity} shows {'increasing' if growth>0 else 'decreasing'} cyber crime trend.
"""

    except Exception as e:
        return f"[ERROR] AI Explanation failed: {e}"


# ================================
# 🧠 STATE INFO ENGINE
# ================================
from src.state_info import STATE_INFO

def get_state_info(state):
    state = state.upper()

    if state not in STATE_INFO:
        return "No data available"

    info = STATE_INFO[state]

    return info

# ================================
# ⚖️ LEGAL INFO ENGINE
# ================================
CRIME_LEGAL_INFO = {
    "data theft": {
        "BNS": "Section 303 (Theft)",
        "IPC": "Section 378",
        "IT_Act": "Section 43, 66",
        "Punishment": "Up to 3 years",
        "Fine": "Up to ₹5 Lakh"
    },
    "extortion": {
        "BNS": "Section 308 (Extortion)",
        "IPC": "Section 383, 384",
        "IT_Act": "Section 66E, 67",
        "Punishment": "Up to 3 to 7 years",
        "Fine": "Discretionary fine"
    },
    "hate crime": {
        "BNS": "Section 196 (Promoting enmity), 299",
        "IPC": "Section 153A, 295A",
        "IT_Act": "Section 66F",
        "Punishment": "Up to 3 to 5 years",
        "Fine": "Discretionary fine"
    },
    "illegal trade": {
        "BNS": "Section 318 (Cheating)",
        "IPC": "Section 415, 420",
        "IT_Act": "Section 66D",
        "Punishment": "Up to 3 to 7 years",
        "Fine": "Discretionary fine"
    },
    "personal revenge": {
        "BNS": "Section 356 (Defamation)",
        "IPC": "Section 499, 500, 506",
        "IT_Act": "Section 66E",
        "Punishment": "Up to 2 to 3 years",
        "Fine": "Up to ₹2 Lakh fine"
    },
    "piracy": {
        "BNS": "Section 318 (Cheating), 303",
        "IPC": "Section 420",
        "IT_Act": "Section 66",
        "Punishment": "6 months to 3 years",
        "Fine": "₹50,000 to ₹2 Lakh"
    },
    "political motive": {
        "BNS": "Section 196 (Promoting enmity), 150",
        "IPC": "Section 153A, 124A",
        "IT_Act": "Section 66F",
        "Punishment": "Up to 3 years to Life",
        "Fine": "Discretionary fine"
    },
    "prank": {
        "BNS": "Section 351 (Criminal Intimidation), 356",
        "IPC": "Section 503, 506",
        "IT_Act": "N/A",
        "Punishment": "Up to 2 years",
        "Fine": "Discretionary fine"
    },
    "sexual exploitation": {
        "BNS": "Section 64 (Rape), 75 (Voyeurism)",
        "IPC": "Section 376, 354C",
        "IT_Act": "Section 67, 67A, 67B",
        "Punishment": "5 to 7 years to Life",
        "Fine": "Up to ₹10 Lakh fine"
    },
    "abetment suicide": {
        "BNS": "Section 108",
        "IPC": "Section 306",
        "IT_Act": "N/A",
        "Punishment": "Up to 10 years",
        "Fine": "Discretionary fine"
    },
    "emotional motive": {
        "BNS": "Section 356 (Defamation), 351",
        "IPC": "Section 499, 506",
        "IT_Act": "Section 66E",
        "Punishment": "Up to 2 years",
        "Fine": "Discretionary fine"
    },
    "fraud": {
        "BNS": "Section 318 (Cheating)",
        "IPC": "Section 415, 420",
        "IT_Act": "Section 66C, 66D",
        "Punishment": "Up to 3 to 7 years",
        "Fine": "Up to ₹1 Lakh fine"
    },
    "terrorism": {
        "BNS": "Section 113",
        "IPC": "Section 121, UAPA",
        "IT_Act": "Section 66F",
        "Punishment": "Life Imprisonment or Death",
        "Fine": "Discretionary fine"
    }
}

def get_crime_legal_info(crime):
    crime = crime.lower().strip()
    return CRIME_LEGAL_INFO.get(crime, {
        "BNS": "N/A",
        "IPC": "N/A",
        "IT_Act": "N/A",
        "Punishment": "N/A",
        "Fine": "N/A"
    })