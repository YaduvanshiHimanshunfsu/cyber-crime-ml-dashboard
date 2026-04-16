"""
=========================================================
🚀 FASTAPI SERVER (PRO MAX VERSION)
=========================================================

Features:
✔ Auto path handling
✔ Safe dataset loading
✔ API validation
✔ Debug logs (terminal)
✔ Error handling (try/except)
✔ Health check endpoint
✔ Production-ready structure

Author: Himanshu Yadav
=========================================================
"""

# ================================
# 📦 IMPORTS
# ================================
import sys
import os
import traceback
from datetime import datetime

# Fix import path (VERY IMPORTANT)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI, Query
import pandas as pd

# Import AI engine
from src.ai_engine import (
    generate_ai_analysis,
    generate_alerts,
    get_hotspots
)

# ================================
# 🚀 INIT APP
# ================================
app = FastAPI(title="Cyber Crime AI API", version="1.0")

print("\n====================================")
print("🚀 STARTING CYBER CRIME API SERVER")
print("====================================")

# ================================
# 📂 PATH CONFIG
# ================================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

DATA_PATH = os.path.join(BASE_DIR, "data/processed/final_dataset.csv")
PRED_PATH = os.path.join(BASE_DIR, "data/processed/future_predictions.csv")

# ================================
# 📊 GLOBAL DATA (CACHE)
# ================================
df = None
pred_df = None


# ================================
# 🔄 SAFE DATA LOADER
# ================================
def load_data():
    global df, pred_df

    print("\n[INFO] Loading datasets...")

    try:
        if not os.path.exists(DATA_PATH):
            raise FileNotFoundError(f"Missing file: {DATA_PATH}")

        if not os.path.exists(PRED_PATH):
            raise FileNotFoundError(f"Missing file: {PRED_PATH}")

        df = pd.read_csv(DATA_PATH)
        pred_df = pd.read_csv(PRED_PATH)

        print(f"[SUCCESS] Dataset loaded: {df.shape}")
        print(f"[SUCCESS] Prediction data loaded: {pred_df.shape}")

    except Exception as e:
        print("[ERROR] Dataset loading failed!")
        print(traceback.format_exc())
        df = pd.DataFrame()
        pred_df = pd.DataFrame()


# Load at startup
load_data()

print("[INFO] ✅ API READY\n")


# ================================
# 🏠 ROOT
# ================================
@app.get("/")
def home():
    return {
        "status": "running",
        "message": "🚀 Cyber Crime AI API is live",
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
        "prediction_loaded": not pred_df.empty
    }


# ================================
# 🔄 RELOAD DATA (ADVANCED FEATURE)
# ================================
@app.get("/reload")
def reload_data():
    load_data()
    return {"message": "🔄 Data reloaded successfully"}


# ================================
# 🤖 AI ANALYSIS
# ================================
@app.get("/analysis")
def get_analysis(
    state: str = Query(..., description="State name"),
    crime: str = Query(..., description="Crime type")
):
    try:
        print(f"\n[API] Analysis request → {state} | {crime}")

        result = generate_ai_analysis(state, crime, df)

        return {
            "status": "success",
            "state": state,
            "crime": crime,
            "analysis": result
        }

    except Exception as e:
        print("[ERROR] Analysis failed")
        print(traceback.format_exc())

        return {
            "status": "error",
            "message": str(e)
        }


# ================================
# 🚨 ALERT SYSTEM
# ================================
@app.get("/alerts")
def get_alerts():
    try:
        print("\n[API] Generating alerts...")

        alerts = generate_alerts(df)

        return {
            "status": "success",
            "total_alerts": len(alerts),
            "alerts": alerts
        }

    except Exception as e:
        print("[ERROR] Alerts failed")
        print(traceback.format_exc())

        return {
            "status": "error",
            "message": str(e)
        }


# ================================
# 🔥 HOTSPOT PREDICTION
# ================================
@app.get("/hotspots")
def get_hotspots():
    try:
        print("\n[API] Calculating hotspots...")

        data = get_hotspots(pred_df)

        return {
            "status": "success",
            "year": int(pred_df["year"].max()) if not pred_df.empty else None,
            "data": data.to_dict(orient="records")
        }

    except Exception as e:
        print("[ERROR] Hotspot failed")
        print(traceback.format_exc())

        return {
            "status": "error",
            "message": str(e)
        }


# ================================
# 🧪 TEST MODE (OPTIONAL)
# ================================
if __name__ == "__main__":
    print("\nRun using:")
    print("uvicorn src.api_server:app --reload\n")