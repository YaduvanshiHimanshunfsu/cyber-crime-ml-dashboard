"""
=========================================================
🚀 CYBER CRIME DATA API (ADVANCED VERSION)
=========================================================

Features:
✔ Smart filtering (case-insensitive)
✔ Self error detection (terminal logs)
✔ Auto data validation
✔ Debug logs
✔ Clean structured responses
✔ Scalable for dashboard + ML + AI

Author: Himanshu Yadav
=========================================================
"""

# ================================
# 📦 IMPORTS
# ================================
import os
import traceback
from datetime import datetime

from fastapi import FastAPI, Query
import pandas as pd

# ================================
# 🚀 INIT APP
# ================================
app = FastAPI(title="Cyber Crime Data API", version="2.0")

print("\n====================================")
print("🚀 STARTING DATA API")
print("====================================")

# ================================
# 📂 PATH CONFIG
# ================================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(BASE_DIR, "data/processed/final_dataset.csv")

# ================================
# 📊 GLOBAL DATA
# ================================
df = None


# ================================
# 🔄 LOAD DATA (SAFE)
# ================================
def load_data():
    global df

    print("\n[INFO] Loading dataset...")

    try:
        if not os.path.exists(DATA_PATH):
            raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

        df = pd.read_csv(DATA_PATH)

        # 🔥 Auto-cleaning
        df["state"] = df["state"].str.strip().str.upper()
        df["category"] = df["category"].str.strip().str.lower()

        print(f"[SUCCESS] Dataset loaded: {df.shape}")

    except Exception as e:
        print("[ERROR] Dataset loading failed!")
        print(traceback.format_exc())
        df = pd.DataFrame()


# Load at startup
load_data()

print("[INFO] ✅ DATA API READY\n")


# ================================
# 🏠 ROOT
# ================================
@app.get("/")
def home():
    return {
        "status": "running",
        "message": "🚀 Cyber Crime Data API",
        "time": str(datetime.now())
    }


# ================================
# ❤️ HEALTH CHECK
# ================================
@app.get("/health")
def health():
    return {
        "status": "ok",
        "data_loaded": not df.empty,
        "rows": int(len(df)) if not df.empty else 0
    }


# ================================
# 🔄 RELOAD DATA
# ================================
@app.get("/reload")
def reload_data():
    load_data()
    return {"message": "🔄 Data reloaded successfully"}


# ================================
# 📍 GET ALL STATES
# ================================
@app.get("/states")
def get_states():
    try:
        states = sorted(df["state"].unique().tolist())

        return {
            "status": "success",
            "total_states": len(states),
            "states": states
        }

    except Exception as e:
        print("[ERROR] States API failed")
        print(traceback.format_exc())

        return {"status": "error", "message": str(e)}


# ================================
# ⚖️ GET ALL CRIMES
# ================================
@app.get("/crimes")
def get_crimes():
    try:
        crimes = sorted(df["category"].unique().tolist())

        return {
            "status": "success",
            "total_crimes": len(crimes),
            "crimes": crimes
        }

    except Exception as e:
        print("[ERROR] Crimes API failed")
        print(traceback.format_exc())

        return {"status": "error", "message": str(e)}


# ================================
# 🏙️ STATE DATA
# ================================
@app.get("/state/{state}")
def get_state_data(state: str):
    try:
        state = state.strip().upper()

        print(f"[API] State request → {state}")

        data = df[df["state"] == state]

        if data.empty:
            return {
                "status": "warning",
                "message": f"No data found for {state}"
            }

        return {
            "status": "success",
            "state": state,
            "records": len(data),
            "data": data.to_dict(orient="records")
        }

    except Exception as e:
        print("[ERROR] State API failed")
        print(traceback.format_exc())

        return {"status": "error", "message": str(e)}


# ================================
# 🔍 CRIME DATA
# ================================
@app.get("/crime/{crime}")
def get_crime_data(crime: str):
    try:
        crime = crime.strip().lower()

        print(f"[API] Crime request → {crime}")

        data = df[df["category"] == crime]

        if data.empty:
            return {
                "status": "warning",
                "message": f"No data found for {crime}"
            }

        return {
            "status": "success",
            "crime": crime,
            "records": len(data),
            "data": data.to_dict(orient="records")
        }

    except Exception as e:
        print("[ERROR] Crime API failed")
        print(traceback.format_exc())

        return {"status": "error", "message": str(e)}


# ================================
# 🔥 FILTER API (ADVANCED)
# ================================
@app.get("/filter")
def filter_data(
    state: str = Query(None),
    crime: str = Query(None),
    year: int = Query(None)
):
    """
    Advanced filtering API
    """

    try:
        data = df.copy()

        print(f"[API] Filter → state={state}, crime={crime}, year={year}")

        if state:
            data = data[data["state"] == state.upper()]

        if crime:
            data = data[data["category"] == crime.lower()]

        if year:
            data = data[data["year"] == year]

        return {
            "status": "success",
            "records": len(data),
            "data": data.to_dict(orient="records")
        }

    except Exception as e:
        print("[ERROR] Filter API failed")
        print(traceback.format_exc())

        return {"status": "error", "message": str(e)}


# ================================
# 📊 SUMMARY API (SMART)
# ================================
@app.get("/summary")
def summary():
    """
    ML-ready aggregated insights
    """

    try:
        summary_df = (
            df.groupby("state")["cases"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        return {
            "status": "success",
            "top_states": summary_df.to_dict()
        }

    except Exception as e:
        print("[ERROR] Summary failed")
        print(traceback.format_exc())

        return {"status": "error", "message": str(e)}


# ================================
# 🧪 TEST MODE
# ================================
if __name__ == "__main__":
    print("\nRun using:")
    print("uvicorn app.api:app --reload\n")