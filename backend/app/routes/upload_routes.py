from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
import pandas as pd

from app.database import get_db
from app.models import HealthcareRecord
from app.services.data_cleaning import clean_healthcare_dataframe

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    try:
        df = pd.read_csv(file.file)
        clean_df, summary = clean_healthcare_dataframe(df)

        # Bulk-create ORM objects and insert in one shot — much faster than row-by-row
        records = [
            HealthcareRecord(
                patient_id=str(row["patient_id"]),
                age=int(row["age"]),
                gender=str(row["gender"]),
                disease=str(row["disease"]),
                hospital=str(row["hospital"]),
                admission_date=row["admission_date"],
                discharge_date=row["discharge_date"],
                length_of_stay=int(row["length_of_stay"]),
                claim_amount=float(row["claim_amount"]),
                claim_status=str(row["claim_status"]),
                city=str(row["city"]),
            )
            for _, row in clean_df.iterrows()
        ]

        db.add_all(records)
        db.commit()

        return {
            "message": "CSV uploaded and processed successfully",
            "file_name": file.filename,
            "rows_inserted": len(records),
            **summary,
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
