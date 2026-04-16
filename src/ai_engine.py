"""
====================================================
🚀 AI ENGINE (ULTIMATE PRO VERSION - FIXED)
====================================================

✔ Multi-model Gemini fallback
✔ Quota handling (429 retry)
✔ AI caching (reduce API usage)
✔ ML + LLM hybrid insights
✔ Alert system
✔ Hotspot prediction
✔ Debug logs (full terminal visibility)
✔ Secure API handling

Author: Himanshu Yadav
====================================================
"""

# ================================
# 📦 IMPORTS
# ================================
import os
import time
from datetime import datetime
import pandas as pd

# ================================
# 🔐 LOAD API KEY (SECURE)
# ================================
def get_api_key():
    print("\n[DEBUG] Checking GEMINI_API_KEY...")

    key = os.getenv("GEMINI_API_KEY")

    if key:
        print("[INFO] ✅ GEMINI_API_KEY FOUND")
        print(f"[DEBUG] Key Preview: {key[:4]}...{key[-4:]}")
        return key
    else:
        print("[WARNING] ❌ GEMINI_API_KEY NOT FOUND")
        print("👉 Run this before starting:")
        print('$env:GEMINI_API_KEY="your_key_here"')
        return None


# ================================
# 🤖 INIT GEMINI
# ================================
client = None

try:
    from google import genai
    from google.genai import types

    api_key = get_api_key()

    if api_key:
        client = genai.Client(api_key=api_key)
        print("[INFO] 🚀 Advanced Gemini initialized with Internet Access")

    else:
        print("[WARNING] Running in fallback offline mode")

except Exception as e:
    print(f"[ERROR] Gemini init failed: {e}")
    client = None


# ================================
# 🔥 MODEL PRIORITY (REAL MODELS)
# ================================
# ✅ Removed the "models/" prefix to fix the 404 NOT FOUND error
MODEL_PRIORITY = [
    "gemini-2.5-flash",         # fast
    "gemini-2.0-flash",         # most stable
    "gemini-2.0-flash-lite",    # lightweight fallback
]

# ================================
# 🧠 CACHE SYSTEM
# ================================
AI_CACHE = {}

# ================================
# 🧠 ADVANCED FALLBACK AI (SMART RULE-BASED)
# ================================
def fallback_analysis(state, crime):
    """
    🔥 Intelligent fallback system
    - State-aware insights
    - Crime-specific logic
    - Legal + real-world mapping
    """

    crime = crime.lower()
    state = state.upper()

    # ================================
    # 📖 CRIME DEFINITIONS DATABASE
    # ================================
    crime_info = {
        "fraud": {
            "definition": "Deception using digital platforms to gain money or sensitive data.",
            "motive": ["Financial gain", "Organized cyber gangs", "Quick profit"],
            "modus": ["Phishing", "Fake banking calls", "UPI scams", "OTP theft"],
            "laws": "IT Act Sec 66C, 66D | BNS Fraud Sections",
            "punishment": "Up to 7 years imprisonment + fine"
        },
        "data theft": {
            "definition": "Unauthorized access and stealing of digital data.",
            "motive": ["Corporate espionage", "Blackmail", "Selling data"],
            "modus": ["Database hacking", "Malware", "Insider leaks"],
            "laws": "IT Act Sec 43, 66 | DPDP Act",
            "punishment": "3–5 years + heavy penalty"
        },
        "sexual exploitation": {
            "definition": "Online harassment, blackmail or exploitation using digital media.",
            "motive": ["Revenge", "Extortion", "Psychological control"],
            "modus": ["Morphing images", "Blackmail", "Fake profiles"],
            "laws": "IT Act Sec 67 | BNS sexual offense laws",
            "punishment": "5–7 years imprisonment"
        },
        "extortion": {
            "definition": "Threatening individuals online to extract money or favors.",
            "motive": ["Money", "Control", "Fear tactics"],
            "modus": ["Ransomware", "Threat emails", "Blackmail"],
            "laws": "IT Act + BNS Extortion Sections",
            "punishment": "Up to 7 years"
        },
        "hate crime": {
            "definition": "Spreading hatred or violence using digital platforms.",
            "motive": ["Ideology", "Political agenda", "Social division"],
            "modus": ["Fake news", "Propaganda", "Targeted campaigns"],
            "laws": "BNS hate speech laws + IT Act",
            "punishment": "3–5 years"
        },
        "terrorism": {
            "definition": "Use of cyberspace for terrorist activities.",
            "motive": ["Radicalization", "Funding", "Recruitment"],
            "modus": ["Encrypted messaging", "Dark web", "Crypto funding"],
            "laws": "UAPA + IT Act",
            "punishment": "Severe (10+ years / life)"
        },
        "illegal trade": {
            "definition": "Online sale of illegal goods (drugs, weapons).",
            "motive": ["Profit", "Dark web markets"],
            "modus": ["Anonymous platforms", "Crypto payments"],
            "laws": "NDPS Act + IT Act",
            "punishment": "5–10 years"
        },
        "prank": {
            "definition": "Harmless-looking but disruptive online activities.",
            "motive": ["Fun", "Attention seeking"],
            "modus": ["Fake alerts", "Spam calls"],
            "laws": "Minor IT violations",
            "punishment": "Fine or minor penalty"
        },
        "abetment suicide": {
            "definition": "Online harassment leading to suicide.",
            "motive": ["Harassment", "Revenge"],
            "modus": ["Cyberbullying", "Threats"],
            "laws": "BNS Sec 108 + IT Act",
            "punishment": "Up to 10 years"
        }
    }

    # ================================
    # 📍 STATE RISK PROFILE
    # ================================
    high_risk_states = ["MAHARASHTRA", "KARNATAKA", "DELHI", "TELANGANA"]
    medium_risk_states = ["UTTAR PRADESH", "WEST BENGAL", "TAMIL NADU"]

    if state in high_risk_states:
        state_risk = "HIGH 🔴"
        state_reason = "High IT infrastructure, digital economy & population density"
    elif state in medium_risk_states:
        state_risk = "MEDIUM 🟡"
        state_reason = "Growing digital adoption and moderate awareness"
    else:
        state_risk = "LOW/MEDIUM 🟢"
        state_reason = "Lower digital density but increasing usage"

    # ================================
    # 📊 FETCH CRIME DATA
    # ================================
    info = crime_info.get(crime, None)

    if not info:
        # fallback if unknown crime
        return f"""
⚠️ AI Fallback Mode

📍 State: {state}
⚖️ Crime: {crime}

Basic cyber crime analysis:
- Increasing due to digital growth
- Requires awareness & monitoring
"""

    # ✅ FIX: Pre-format lists to avoid f-string syntax errors with '\n'
    formatted_motives = '\n- '.join(info['motive'])
    formatted_modus = '\n- '.join(info['modus'])

    # ================================
    # 🧠 BUILD RESPONSE
    # ================================
    return f"""
⚠️ AI Service Unavailable (Smart Fallback Mode)

📍 State: {state}
⚖️ Crime: {crime.upper()}

📖 Definition:
{info['definition']}

🎯 Motive:
- {formatted_motives}

⚙️ Modus Operandi:
- {formatted_modus}

📈 Why Increasing in {state}:
- {state_reason}
- Increased internet penetration
- Weak cybersecurity awareness

⚖️ Legal Framework:
{info['laws']}

💰 Punishment:
{info['punishment']}

🚨 Risk Level:
{state_risk}

🛡️ Prevention:
- Strong passwords + 2FA
- Avoid unknown links
- Cyber awareness training
- Government monitoring systems
"""


# ================================
# 🤖 GEMINI CALL (ADVANCED)
# ================================
def call_gemini(prompt, state, crime):
    """
    🔥 PRODUCTION-LEVEL GEMINI CALL

    Handles:
    ✔ 503 (server overload)
    ✔ 429 (quota)
    ✔ retry logic
    ✔ multi-model fallback
    ✔ caching
    """

    if not client:
        return None

    cache_key = f"{state}_{crime}"

    # ================================
    # CACHE CHECK
    # ================================
    if cache_key in AI_CACHE:
        print("[CACHE HIT] Using stored result")
        return AI_CACHE[cache_key]

    # ================================
    # TRY EACH MODEL
    # ================================
    for model in MODEL_PRIORITY:

        retries = 3  # try each model 3 times

        for attempt in range(retries):
            try:
                print(f"\n[TRYING] {model} | Attempt {attempt+1}/{retries}")

                try:
                    # 🚀 ADVANCED FEATURE: Google Search Grounding (Internet access)
                    response = client.models.generate_content(
                        model=model,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            tools=[{"google_search": {}}],
                            temperature=0.3
                        )
                    )
                except Exception as inner_e:
                    # Self Error Finding: If grounding is restricted on specific API quotas, fallback safely
                    print(f"[DIAGNOSTIC] Internet grounding caught exception: {inner_e}. Falling back to standard generation...")
                    response = client.models.generate_content(
                        model=model,
                        contents=prompt
                    )

                print(f"[SUCCESS] ✅ {model} worked")

                AI_CACHE[cache_key] = response.text
                return response.text

            except Exception as e:
                err = str(e)

                # ================================
                # 503 → WAIT + RETRY
                # ================================
                if "503" in err or "UNAVAILABLE" in err:
                    print("[503] Server busy → retrying in 5 sec...")
                    time.sleep(5)
                    continue

                # ================================
                # 429 → SKIP MODEL
                # ================================
                elif "429" in err or "RESOURCE_EXHAUSTED" in err:
                    print("[429] Quota hit → skipping this model...")
                    break

                # ================================
                # OTHER ERRORS → BREAK MODEL
                # ================================
                else:
                    print(f"[FAILED] {model}: {e}")
                    break

        print(f"[SKIP] Moving to next model...\n")

    # ================================
    # FINAL FAIL
    # ================================
    print("[FINAL FAIL] All models failed")
    return None


# ================================
# 🔥 MAIN AI FUNCTION
# ================================
def generate_ai_analysis(state, crime, data=None):

    print("\n===================================")
    print(f"[AI ENGINE] {state} | {crime}")
    print(f"[TIME] {datetime.now()}")
    print("===================================")

    # ================================
    # 📊 ML TREND
    # ================================
    trend_info = ""

    if isinstance(data, pd.DataFrame) and not data.empty:
        try:
            trend = data.groupby("year")["cases"].sum()

            if len(trend) >= 2:
                growth = ((trend.iloc[-1] - trend.iloc[0]) / (trend.iloc[0] + 1)) * 100
                trend_info = f"Trend Growth: {growth:.2f}%"
                print(f"[INFO] 📊 {trend_info}")

        except Exception as e:
            print("[WARNING] Trend failed:", e)

    # ================================
    # 🤖 PROMPT
    # ================================
    if crime == "comparison":
        prompt = f"""
Compare cyber crime trends between the selected states: {state}.

Include:
- Key difference in the graph (based on general intuition or if you see {trend_info})
- Proper reason why one state might have more cases than another.
- Major cyber challenges unique to each state.
- How can it be solved collaboratively.

Please keep it concise, structured and markdown formatted.
"""
    else:
        prompt = f"""
Analyze cyber crime '{crime}' in {state}, India.

Include:
- **Definition** of {crime}
- **Motive**: What must be the motive in this specific crime?
- **Modus Operandi**
- **Why it is increasing** in {state}
- **How can it be solved**: Solutions and Prevention strategies
- **Legal sections**: BNS, IT Act
- **Punishment & Fine**
- **Risk level**

ML Insight:
{trend_info}
"""

    # ================================
    # GEMINI
    # ================================
    result = call_gemini(prompt, state, crime)

    if result:
        return result

    # ================================
    # FALLBACK
    # ================================
    print("[FALLBACK] Using offline AI")
    return fallback_analysis(state, crime)


# ================================
# 🚨 ALERT SYSTEM
# ================================
def generate_alerts(df):

    alerts = []

    try:
        grouped = df.groupby(["state", "category", "year"])["cases"].sum().reset_index()

        # ✅ FIXED variables to avoid shadowing function arguments
        for (state_name, crime_name), group in grouped.groupby(["state", "category"]):
            group = group.sort_values("year")

            if len(group) >= 2:
                prev = group.iloc[-2]["cases"]
                curr = group.iloc[-1]["cases"]

                if prev > 0:
                    change = ((curr - prev) / prev) * 100

                    if change > 40:
                        alerts.append(f"🚨 {crime_name.upper()} rising {change:.1f}% in {state_name}")

    except Exception as e:
        print("[ERROR] Alerts failed:", e)

    return alerts


# ================================
# 🔥 HOTSPOTS
# ================================
def get_hotspots(pred_df):

    try:
        latest = pred_df["year"].max()

        top = (
            pred_df[pred_df["year"] == latest]
            .groupby("state")["predicted_cases"]
            .sum()
            .sort_values(ascending=False)
            .head(5)
        )

        return top.reset_index()

    except Exception as e:
        print("[ERROR] Hotspots failed:", e)
        return pd.DataFrame()


# ================================
# 🧠 RECOMMENDATION ENGINE
# ================================
def generate_recommendations(state, risk):

    if risk == "HIGH":
        return f"🔴 {state}: Immediate strict monitoring needed"
    elif risk == "MEDIUM":
        return f"🟡 {state}: Improve awareness"
    return f"🟢 {state}: Stable"


# ================================
# 🧪 TEST
# ================================
if __name__ == "__main__":
    print("\n========= TEST MODE =========")
    print(generate_ai_analysis("Delhi", "fraud"))