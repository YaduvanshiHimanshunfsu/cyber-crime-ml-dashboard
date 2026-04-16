import os
import pandas as pd
import numpy as np
import pickle

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split

# Optional
try:
    from xgboost import XGBRegressor
    XGB_AVAILABLE = True
except:
    XGB_AVAILABLE = False


# ================================
# CONFIG
# ================================
DATA_PATH = "data/processed/ml_ready_dataset.csv"
MODEL_PATH = "models/cybercrime_model.pkl"
PRED_PATH = "data/processed/future_predictions.csv"

FEATURE_COLS = [
    "year",
    "lag_1",
    "lag_2",
    "rolling_mean_3",
    "growth_rate",
    "state_encoded",
    "category_encoded"
]


# ================================
# LOAD DATA
# ================================
def load_data():
    print("[INFO] Loading dataset...")

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError("Dataset not found!")

    df = pd.read_csv(DATA_PATH)
    print(f"[INFO] Dataset loaded: {df.shape}")

    return df


# ================================
# CLEAN FEATURES
# ================================
def clean_features(X):
    print("[INFO] Cleaning feature matrix...")

    X = X.replace([np.inf, -np.inf], np.nan)
    X = X.fillna(0)

    print("[INFO] Feature cleaning complete")
    return X


# ================================
# TRAIN MODELS
# ================================
def train_models(X, y):
    print("[INFO] Splitting dataset...")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    models = {}

    # ===== RandomForest =====
    print("[INFO] Training RandomForest...")
    rf = RandomForestRegressor(n_estimators=200, random_state=42)
    rf.fit(X_train, y_train)
    models["rf"] = rf

    # ===== XGBoost =====
    if XGB_AVAILABLE:
        print("[INFO] Training XGBoost...")
        xgb = XGBRegressor(n_estimators=200, learning_rate=0.05)
        xgb.fit(X_train, y_train)
        models["xgb"] = xgb

    # ===== Evaluation =====
    print("[INFO] Evaluating models...")

    best_model = None
    best_rmse = float("inf")

    for name, model in models.items():
        preds = model.predict(X_test)

        mae = mean_absolute_error(y_test, preds)
        rmse = np.sqrt(mean_squared_error(y_test, preds))

        print(f"\n📊 {name.upper()}")
        print(f"MAE : {mae:.2f}")
        print(f"RMSE: {rmse:.2f}")

        if rmse < best_rmse:
            best_rmse = rmse
            best_model = model

    return best_model, X_test, y_test


# ================================
# FUTURE PREDICTION (FIXED)
# ================================
def generate_future_predictions(df, model):
    print("[INFO] Generating predictions till 2028...")

    future_rows = []

    grouped = df.groupby(["state", "category"])

    for (state, category), group in grouped:
        group = group.sort_values("year")

        last_row = group.iloc[-1].copy()

        for year in range(2024, 2029):

            # ===== UPDATE FEATURES =====
            lag_1 = last_row["cases"]
            lag_2 = last_row["lag_1"]
            rolling = (lag_1 + lag_2) / 2

            growth = (lag_1 - lag_2) / (lag_2 + 1)

            # ✅ FIX: USE DATAFRAME WITH COLUMN NAMES
            input_df = pd.DataFrame([{
                "year": year,
                "lag_1": lag_1,
                "lag_2": lag_2,
                "rolling_mean_3": rolling,
                "growth_rate": growth,
                "state_encoded": last_row["state_encoded"],
                "category_encoded": last_row["category_encoded"]
            }])

            # Ensure same column order
            input_df = input_df[FEATURE_COLS]

            # ===== PREDICT =====
            pred = model.predict(input_df)[0]

            pred = max(0, pred)  # no negative crimes 😄

            future_rows.append({
                "state": state,
                "category": category,
                "year": year,
                "predicted_cases": pred
            })

            # update for next iteration
            last_row["cases"] = pred
            last_row["lag_1"] = lag_1

    future_df = pd.DataFrame(future_rows)

    os.makedirs(os.path.dirname(PRED_PATH), exist_ok=True)
    future_df.to_csv(PRED_PATH, index=False)

    print(f"[INFO] Predictions saved at {PRED_PATH}")


# ================================
# MAIN
# ================================
def main():
    print("\n========= 🚀 TRAINING MODEL =========\n")

    try:
        df = load_data()

        print("[INFO] Preparing features...")

        X = df[FEATURE_COLS]
        y = df["cases"]

        X = clean_features(X)

        model, X_test, y_test = train_models(X, y)

        os.makedirs("models", exist_ok=True)

        with open(MODEL_PATH, "wb") as f:
            pickle.dump(model, f)

        print(f"[INFO] Model saved at {MODEL_PATH}")

        generate_future_predictions(df, model)

        print("\n========= ✅ TRAINING COMPLETE =========")

    except Exception as e:
        print("\n[ERROR] Pipeline failed!")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()