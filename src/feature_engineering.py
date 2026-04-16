import pandas as pd
import numpy as np
import os

print("\n========= 🚀 FEATURE ENGINEERING =========\n")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_PATH = os.path.join(BASE_DIR, "data", "processed", "final_dataset.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "processed", "ml_ready_dataset.csv")

# ============================================
# LOAD DATA
# ============================================

try:
    df = pd.read_csv(INPUT_PATH)
except Exception as e:
    print("[ERROR] Cannot load dataset:", e)
    exit()

# ============================================
# CLEAN BASIC
# ============================================

df["state"] = df["state"].astype(str).str.strip().str.upper()
df["category"] = df["category"].astype(str).str.strip().str.lower()
df["year"] = pd.to_numeric(df["year"], errors="coerce")
df["cases"] = pd.to_numeric(df["cases"], errors="coerce")

df = df.dropna(subset=["state", "category", "year", "cases"])

# ============================================
# 🔥 CRITICAL FIX → REMOVE DUPLICATES
# ============================================

df = (
    df.groupby(["state", "category", "year"], as_index=False)["cases"]
    .sum()
)

print(f"[INFO] After aggregation: {df.shape}")

# ============================================
# FILL MISSING YEARS (SAFE VERSION)
# ============================================

ALL_YEARS = list(range(int(df["year"].min()), int(df["year"].max()) + 1))

def fill_missing_years(group):
    group = group.set_index("year")

    # Remove duplicate index if still any (extra safety)
    group = group[~group.index.duplicated(keep="first")]

    group = group.reindex(ALL_YEARS)

    # Forward fill safely
    group["state"] = group["state"].ffill()
    group["category"] = group["category"].ffill()

    # Fill missing cases (0 or interpolate)
    group["cases"] = group["cases"].interpolate(method="linear").fillna(0)

    return group.reset_index()

df = (
    df.groupby(["state", "category"], group_keys=False)
    .apply(fill_missing_years)
    .reset_index(drop=True)
)

print(f"[INFO] After filling years: {df.shape}")

# ============================================
# FEATURE ENGINEERING (ADVANCED)
# ============================================

df = df.sort_values(["state", "category", "year"])

# Lag Features
df["lag_1"] = df.groupby(["state", "category"])["cases"].shift(1)
df["lag_2"] = df.groupby(["state", "category"])["cases"].shift(2)

# Rolling Mean
df["rolling_mean_3"] = (
    df.groupby(["state", "category"])["cases"]
    .rolling(3)
    .mean()
    .reset_index(level=[0,1], drop=True)
)

# Growth Rate
df["growth_rate"] = (
    df.groupby(["state", "category"])["cases"]
    .pct_change()
)

# Replace NaNs
df = df.fillna(0)

# ============================================
# ENCODING
# ============================================

df["state_encoded"] = df["state"].astype("category").cat.codes
df["category_encoded"] = df["category"].astype("category").cat.codes

# ============================================
# SAVE
# ============================================

df.to_csv(OUTPUT_PATH, index=False)

print("\n========= ✅ FEATURE ENGINEERING COMPLETE =========")
print(f"[INFO] Saved at: {OUTPUT_PATH}")
print(df.head())