from fastapi import FastAPI
import pandas as pd

app = FastAPI(title="Cyber Crime API")

DATA_PATH = "data/processed/final_dataset.csv"

df = pd.read_csv(DATA_PATH)


# ================================
# GET ALL STATES
# ================================
@app.get("/states")
def get_states():
    return sorted(df["state"].unique().tolist())


# ================================
# GET STATE DATA
# ================================
@app.get("/state/{state}")
def get_state_data(state: str):
    data = df[df["state"] == state.upper()]
    return data.to_dict(orient="records")


# ================================
# GET CRIME DATA
# ================================
@app.get("/crime/{crime}")
def get_crime_data(crime: str):
    data = df[df["category"] == crime.lower()]
    return data.to_dict(orient="records")