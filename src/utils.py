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

    