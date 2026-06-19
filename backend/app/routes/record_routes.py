from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import HealthcareRecord
from app.schemas import RecordCreate, RecordResponse

router = APIRouter(prefix="/records", tags=["Records"])


@router.post("", response_model=RecordResponse)
def add_record(payload: RecordCreate, db: Session = Depends(get_db)):
    length_of_stay = (payload.discharge_date - payload.admission_date).days
    if length_of_stay < 0:
        raise HTTPException(status_code=400, detail="discharge_date cannot be before admission_date")

    record = HealthcareRecord(
        patient_id=payload.patient_id.strip(),
        age=payload.age,
        gender=payload.gender.strip().title(),
        disease=payload.disease.strip(),
        hospital=payload.hospital.strip(),
        admission_date=payload.admission_date,
        discharge_date=payload.discharge_date,
        length_of_stay=length_of_stay,
        claim_amount=payload.claim_amount,
        claim_status=payload.claim_status.strip().title(),
        city=payload.city.strip(),
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/recent")
def get_recent_records(db: Session = Depends(get_db)):
    records = db.query(HealthcareRecord).order_by(HealthcareRecord.created_at.desc()).limit(10).all()
    return records
