from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.analytics_service import (
    get_summary,
    get_patient_trends,
    get_disease_distribution,
    get_hospital_performance,
    get_claim_costs,
    get_claim_status_distribution,
    get_insights,
)

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    return get_summary(db)


@router.get("/patient-trends")
def patient_trends(db: Session = Depends(get_db)):
    return get_patient_trends(db)


@router.get("/disease-distribution")
def disease_distribution(db: Session = Depends(get_db)):
    return get_disease_distribution(db)


@router.get("/hospital-performance")
def hospital_performance(db: Session = Depends(get_db)):
    return get_hospital_performance(db)


@router.get("/claim-costs")
def claim_costs(db: Session = Depends(get_db)):
    return get_claim_costs(db)


@router.get("/claim-status")
def claim_status(db: Session = Depends(get_db)):
    return get_claim_status_distribution(db)


@router.get("/insights")
def insights(db: Session = Depends(get_db)):
    return {"insights": get_insights(db)}
