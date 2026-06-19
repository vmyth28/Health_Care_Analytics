from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
import os
from app.database import Base, engine, SessionLocal
from app.routes import upload_routes, record_routes, analytics_routes, ml_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Healthcare Analytics and Prediction API",
    description="FastAPI backend for healthcare analytics dashboard",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_routes.router)
app.include_router(record_routes.router)
app.include_router(analytics_routes.router)
app.include_router(ml_routes.router)

origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Healthcare Analytics API is running successfully"}


@app.get("/api/test")
def test_api():
    return {"status": "success", "message": "Frontend and Backend are connected successfully"}


@app.get("/api/db-test")
def db_test():
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        return {"status": "success", "message": "Database connected successfully"}
    finally:
        db.close()
