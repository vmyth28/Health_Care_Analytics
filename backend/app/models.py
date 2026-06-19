from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from datetime import datetime
from app.database import Base


class HealthcareRecord(Base):
    __tablename__ = "healthcare_records"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, index=True, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    disease = Column(String, nullable=False)
    hospital = Column(String, nullable=False)
    admission_date = Column(Date, nullable=False)
    discharge_date = Column(Date, nullable=False)
    length_of_stay = Column(Integer, nullable=False)
    claim_amount = Column(Float, nullable=False)
    claim_status = Column(String, nullable=False)
    city = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
