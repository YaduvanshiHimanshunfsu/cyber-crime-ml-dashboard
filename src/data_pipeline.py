import os
import re
import pandas as pd
from difflib import get_close_matches

# ================================
# CONFIGURATION
# ================================
# Folder containing raw NCRB CSV files
DATA_FOLDER = "data/raw"

# Output cleaned dataset
OUTPUT_FILE = "data/processed/final_dataset.csv"


# ================================
# MASTER STATE LIST (STANDARDIZED)
# ================================
# This ensures uniform naming for ML models
STANDARD_STATES = [
    "ANDAMAN AND NICOBAR ISLANDS", "ANDHRA PRADESH", "ARUNACHAL PRADESH",
    "ASSAM", "BIHAR", "CHANDIGARH", "CHHATTISGARH",
    "DADRA AND NAGAR HAVELI", "DAMAN AND DIU", "DELHI",
    "GOA", "GUJARAT", "HARYANA", "HIMACHAL PRADESH",
    "JAMMU AND KASHMIR", "JHARKHAND", "KARNATAKA", "KERALA",
    "LADAKH", "LAKSHADWEEP", "MADHYA PRADESH", "MAHARASHTRA",
    "MANIPUR", "MEGHALAYA", "MIZORAM", "NAGALAND",
    "ODISHA", "PUDUCHERRY", "PUNJAB", "RAJASTHAN",
    "SIKKIM", "TAMIL NADU", "TELANGANA", "TRIPURA",
    "UTTAR PRADESH", "UTTARAKHAND", "WEST BENGAL"
]

# Track unknown states for debugging
unknown_states = set()


# ================================
# REMOVE INVALID / TOTAL ROWS
# ================================
def is_invalid_state(val):
    """
    Detects aggregate rows like TOTAL, INDIA, etc.
    These should NOT be used for ML training.
    """
    val = str(val).strip().upper()

    patterns = [
        r"^TOTAL",
        r"ALL INDIA",
        r"^INDIA",
        r"^TOTAL STATE",
        r"^TOTAL UT",
        r"\(TOTAL",
        r"GRAND TOTAL"
    ]

    for p in patterns:
        if re.search(p, val):
            return True

    return False


# ================================
# STATE NORMALIZATION (ADVANCED)
# ================================
def normalize_state(name):
    """
    Converts messy state names into standardized format.
    Handles:
    - Short forms (A&N, D&N)
    - Symbols (&, special chars)
    - Fuzzy matching
    """
    original = str(name)
    name = original.strip().upper()

    # ---- Special cases (critical fixes) ----
    if re.search(r"D\s*&\s*N", name) or "DADRA" in name or "NAGAR HAVELI" in name:
        return "DADRA AND NAGAR HAVELI"

    if re.search(r"DAMAN|DIU", name):
        return "DAMAN AND DIU"

    if re.search(r"A\s*&\s*N", name) or "NICOBAR" in name:
        return "ANDAMAN AND NICOBAR ISLANDS"

    if "JAMMU" in name and "KASHMIR" in name:
        return "JAMMU AND KASHMIR"

    if "DELHI" in name:
        return "DELHI"

    # ---- Clean symbols and spaces ----
    name = name.replace("&", " AND ")
    name = re.sub(r"[^\w\s]", " ", name)
    name = re.sub(r"\s+", " ", name).strip()

    # ---- Fuzzy matching ----
    match = get_close_matches(name, STANDARD_STATES, n=1, cutoff=0.80)
    if match:
        return match[0]

    # ---- Unknown fallback ----
    unknown_states.add(original)
    return name


# ================================
# CATEGORY NORMALIZATION
# ================================
CATEGORY_MAP = {
    "fraud": "fraud",
    "extortion": "extortion",
    "sexual": "sexual exploitation",
    "revenge": "personal revenge",
    "anger": "emotional motive",
    "hate": "hate crime",
    "drug": "illegal trade",
    "piracy": "piracy",
    "prank": "prank",
    "suicide": "abetment suicide",
    "information": "data theft",
    "theft": "data theft",
    "terror": "terrorism",
    "political": "political motive"
}

def normalize_category(col):
    """
    Maps messy column names to standardized crime categories.
    """
    col = col.lower()

    for key, val in CATEGORY_MAP.items():
        if key in col:
            return val

    return "other"


# ================================
# EXTRACT YEAR FROM FILENAME
# ================================
def extract_year(filename):
    match = re.search(r"(20\d{2})", filename)
    return int(match.group(1)) if match else None


# ================================
# PROCESS EACH FILE
# ================================
def process_file(filepath):
    print(f"\n[PROCESSING] {os.path.basename(filepath)}")

    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        print(f"[ERROR] Cannot read file: {e}")
        return pd.DataFrame()

    print(f"[DEBUG] Columns: {list(df.columns)}")

    # ---- Detect state column ----
    state_col = None
    for col in df.columns:
        if "state" in col.lower():
            state_col = col
            break

    if not state_col:
        print("[ERROR] No state column found")
        return pd.DataFrame()

    # ---- Remove TOTAL rows BEFORE normalization ----
    df = df[~df[state_col].apply(is_invalid_state)]

    # ---- Debug sample ----
    print("\n[DEBUG] Raw States Sample:")
    print(df[state_col].dropna().unique()[:10])

    # ---- Normalize states ----
    df["state"] = df[state_col].apply(normalize_state)

    print("\n[DEBUG] Normalized States Sample:")
    print(df["state"].unique()[:10])

    # ---- Extract year ----
    year = extract_year(filepath)
    if not year:
        print("[WARNING] Year not found, skipping file")
        return pd.DataFrame()

    # ---- Extract records ----
    records = []

    for col in df.columns:
        if col == state_col:
            continue

        if "total" in col.lower():
            continue

        category = normalize_category(col)

        if category == "other":
            continue

        for _, row in df.iterrows():
            try:
                value = float(row[col]) if pd.notna(row[col]) else 0
            except:
                value = 0

            records.append({
                "state": row["state"],
                "year": year,
                "category": category,
                "cases": value,
                "source": os.path.basename(filepath)
            })

    print(f"[INFO] Extracted rows: {len(records)}")

    return pd.DataFrame(records)


# ================================
# MAIN PIPELINE
# ================================
def main():
    print("\n========= 🚀 START DATA PIPELINE =========\n")

    all_data = []

    for file in os.listdir(DATA_FOLDER):
        if file.endswith(".csv"):
            filepath = os.path.join(DATA_FOLDER, file)
            df = process_file(filepath)
            if not df.empty:
                all_data.append(df)

    if not all_data:
        print("[ERROR] No data processed")
        return

    df_final = pd.concat(all_data, ignore_index=True)

    print("\n[INFO] Cleaning dataset...")

    # ---- Ensure numeric ----
    df_final["cases"] = pd.to_numeric(df_final["cases"], errors="coerce").fillna(0)

    # ---- Aggregate ----
    df_final = df_final.groupby(
        ["state", "year", "category"], as_index=False
    )["cases"].sum()

    # ================================
    # FINAL DEBUG REPORT
    # ================================
    print("\n========= 🔍 FINAL DEBUG =========")

    print("\n✔ ALL STATES:")
    for s in sorted(df_final["state"].unique()):
        print(f" → {s}")

    print("\n⚠ UNKNOWN STATES:")
    if unknown_states:
        for s in unknown_states:
            print(f" → {s}")
    else:
        print(" → NONE")

    print(f"\nTotal States: {df_final['state'].nunique()}")
    print(f"Total Categories: {df_final['category'].nunique()}")

    # ================================
    # SAVE OUTPUT
    # ================================
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    df_final.to_csv(OUTPUT_FILE, index=False)

    print("\n========= ✅ PIPELINE COMPLETE =========")
    print(f"[INFO] Saved at: {OUTPUT_FILE}")
    print(df_final.head())


# ================================
# ENTRY POINT
# ================================
if __name__ == "__main__":
    main()