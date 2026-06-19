import pandas as pd

REQUIRED_COLUMNS = [
    "patient_id", "age", "gender", "disease", "hospital",
    "admission_date", "discharge_date", "claim_amount", "claim_status", "city"
]


def clean_healthcare_dataframe(df: pd.DataFrame):
    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]

    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    total_records = len(df)

    df = df[REQUIRED_COLUMNS]
    df = df.drop_duplicates()
    df = df.dropna(subset=REQUIRED_COLUMNS)

    for col in ["patient_id", "gender", "disease", "hospital", "claim_status", "city"]:
        df[col] = df[col].astype(str).str.strip()

    df["gender"] = df["gender"].str.title()
    df["claim_status"] = df["claim_status"].str.title()
    df = df[df["claim_status"].isin(["Approved", "Rejected", "Pending"])]

    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    df["claim_amount"] = (
        df["claim_amount"]
        .astype(str)
        .str.replace("₹", "", regex=False)
        .str.replace(",", "", regex=False)
    )
    df["claim_amount"] = pd.to_numeric(df["claim_amount"], errors="coerce")

    df["admission_date"] = pd.to_datetime(df["admission_date"], errors="coerce")
    df["discharge_date"] = pd.to_datetime(df["discharge_date"], errors="coerce")

    df = df.dropna(subset=["age", "claim_amount", "admission_date", "discharge_date"])
    df = df[(df["age"] >= 0) & (df["age"] <= 120)]
    df = df[df["claim_amount"] >= 0]

    df["length_of_stay"] = (df["discharge_date"] - df["admission_date"]).dt.days
    df = df[df["length_of_stay"] >= 0]

    df["age"] = df["age"].astype(int)
    df["admission_date"] = df["admission_date"].dt.date
    df["discharge_date"] = df["discharge_date"].dt.date

    valid_records = len(df)
    invalid_records = total_records - valid_records

    return df, {
        "total_records": int(total_records),
        "valid_records": int(valid_records),
        "invalid_records": int(invalid_records),
    }
