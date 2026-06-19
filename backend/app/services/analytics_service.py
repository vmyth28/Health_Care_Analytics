import pandas as pd
from sqlalchemy.orm import Session
from app.models import HealthcareRecord


def records_to_dataframe(db: Session):
    records = db.query(HealthcareRecord).all()
    data = []
    for r in records:
        data.append({
            "id": r.id,
            "patient_id": r.patient_id,
            "age": r.age,
            "gender": r.gender,
            "disease": r.disease,
            "hospital": r.hospital,
            "admission_date": r.admission_date,
            "discharge_date": r.discharge_date,
            "length_of_stay": r.length_of_stay,
            "claim_amount": r.claim_amount,
            "claim_status": r.claim_status,
            "city": r.city,
            "created_at": r.created_at,
        })
    return pd.DataFrame(data)


def get_summary(db: Session):
    df = records_to_dataframe(db)
    if df.empty:
        return {
            "total_patients": 0,
            "total_claim_amount": 0,
            "average_claim_amount": 0,
            "most_common_disease": "N/A",
            "top_hospital": "N/A",
            "approved_claims": 0,
            "rejected_claims": 0,
            "pending_claims": 0,
        }

    status_counts = df["claim_status"].value_counts().to_dict()
    return {
        "total_patients": int(len(df)),
        "total_claim_amount": round(float(df["claim_amount"].sum()), 2),
        "average_claim_amount": round(float(df["claim_amount"].mean()), 2),
        "most_common_disease": str(df["disease"].mode().iloc[0]),
        "top_hospital": str(df["hospital"].mode().iloc[0]),
        "approved_claims": int(status_counts.get("Approved", 0)),
        "rejected_claims": int(status_counts.get("Rejected", 0)),
        "pending_claims": int(status_counts.get("Pending", 0)),
    }


def get_patient_trends(db: Session):
    df = records_to_dataframe(db)
    if df.empty:
        return []
    df["admission_date"] = pd.to_datetime(df["admission_date"])
    trends = df.groupby(df["admission_date"].dt.strftime("%Y-%m")).size().reset_index(name="patients")
    trends = trends.rename(columns={"admission_date": "month"})
    return trends.to_dict(orient="records")


def get_disease_distribution(db: Session):
    df = records_to_dataframe(db)
    if df.empty:
        return []
    result = df["disease"].value_counts().reset_index()
    result.columns = ["disease", "count"]
    return result.to_dict(orient="records")


def get_hospital_performance(db: Session):
    df = records_to_dataframe(db)
    if df.empty:
        return []
    result = df.groupby("hospital").agg(
        patient_count=("patient_id", "count"),
        average_claim_amount=("claim_amount", "mean"),
        average_stay=("length_of_stay", "mean"),
    ).reset_index()
    result["average_claim_amount"] = result["average_claim_amount"].round(2)
    result["average_stay"] = result["average_stay"].round(2)
    return result.to_dict(orient="records")


def get_claim_costs(db: Session):
    df = records_to_dataframe(db)
    if df.empty:
        return {
            "total_claim_amount": 0,
            "average_claim_amount": 0,
            "highest_claim_amount": 0,
            "lowest_claim_amount": 0,
            "claim_by_disease": [],
        }
    claim_by_disease = df.groupby("disease")["claim_amount"].mean().reset_index()
    claim_by_disease.columns = ["disease", "average_claim_amount"]
    claim_by_disease["average_claim_amount"] = claim_by_disease["average_claim_amount"].round(2)
    return {
        "total_claim_amount": round(float(df["claim_amount"].sum()), 2),
        "average_claim_amount": round(float(df["claim_amount"].mean()), 2),
        "highest_claim_amount": round(float(df["claim_amount"].max()), 2),
        "lowest_claim_amount": round(float(df["claim_amount"].min()), 2),
        "claim_by_disease": claim_by_disease.to_dict(orient="records"),
    }


def get_claim_status_distribution(db: Session):
    df = records_to_dataframe(db)
    if df.empty:
        return []
    result = df["claim_status"].value_counts().reset_index()
    result.columns = ["status", "count"]
    return result.to_dict(orient="records")


def get_insights(db: Session):
    df = records_to_dataframe(db)
    if df.empty:
        return ["No data available. Upload CSV or add records to generate insights."]

    insights = []
    most_common_disease = df["disease"].mode().iloc[0]
    top_hospital = df["hospital"].mode().iloc[0]
    avg_claim = df["claim_amount"].mean()
    highest_claim_disease = df.groupby("disease")["claim_amount"].mean().idxmax()
    approval_rate = (df["claim_status"].eq("Approved").mean()) * 100

    insights.append(f"{most_common_disease} is the most common disease in the dataset.")
    insights.append(f"{top_hospital} handled the maximum number of patient records.")
    insights.append(f"Average claim amount is ₹{avg_claim:,.2f}.")
    insights.append(f"{highest_claim_disease} has the highest average claim amount.")
    insights.append(f"Claim approval rate is {approval_rate:.2f}%.")

    return insights
