from datetime import date, datetime
from pydantic import BaseModel, Field, field_validator, model_validator


class RecordCreate(BaseModel):
    patient_id: str = Field(..., min_length=1)
    age: int = Field(..., ge=0, le=120)
    gender: str
    disease: str
    hospital: str
    admission_date: date
    discharge_date: date
    claim_amount: float = Field(..., ge=0)
    claim_status: str
    city: str

    @field_validator("claim_status")
    @classmethod
    def validate_claim_status(cls, value):
        allowed = {"Approved", "Rejected", "Pending"}
        value = value.strip().title()
        if value not in allowed:
            raise ValueError("claim_status must be Approved, Rejected, or Pending")
        return value

    @field_validator("gender")
    @classmethod
    def normalize_gender(cls, value):
        return value.strip().title()

    @model_validator(mode="after")
    def validate_dates(self):
        if self.discharge_date < self.admission_date:
            raise ValueError("discharge_date cannot be before admission_date")
        return self


class RecordResponse(RecordCreate):
    id: int
    length_of_stay: int
    created_at: datetime

    class Config:
        from_attributes = True


class ClaimPredictionRequest(BaseModel):
    age: int = Field(..., ge=0, le=120)
    gender: str
    disease: str
    hospital: str
    admission_date: date
    discharge_date: date
    city: str

    @model_validator(mode="after")
    def validate_dates(self):
        if self.discharge_date < self.admission_date:
            raise ValueError("discharge_date cannot be before admission_date")
        return self
