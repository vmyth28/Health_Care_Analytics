from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ClaimPredictionRequest
from app.services.ml_service import train_claim_model, predict_claim_amount

router = APIRouter(prefix="/ml", tags=["Machine Learning"])


@router.post("/train")
def train_model(db: Session = Depends(get_db)):
    return train_claim_model(db)


@router.post("/predict-claim")
def predict_claim(payload: ClaimPredictionRequest):
    return predict_claim_amount(payload)
