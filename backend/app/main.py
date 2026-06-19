from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
import os
import logging
from dotenv import load_dotenv
from app.database import Base, engine, SessionLocal
from app.routes import upload_routes, record_routes, analytics_routes, ml_routes

load_dotenv()

logger = logging.getLogger("uvicorn.error")

try:
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Database tables created/verified successfully.")
except Exception as e:
    logger.error(f"❌ Could not connect to the database on startup: {e}")
    logger.error("Check your DATABASE_URL environment variable and make sure special characters in the password are URL-encoded (@ → %40, # → %23, etc.)")

app = FastAPI(
    title="Healthcare Analytics and Prediction API",
    description="FastAPI backend for healthcare analytics dashboard",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_routes.router)
app.include_router(record_routes.router)
app.include_router(analytics_routes.router)
app.include_router(ml_routes.router)

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
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        db.close()


@app.get("/api/health")
def health_check():
    """Quick liveness probe — always returns 200 even if DB is down."""
    db_ok = False
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        pass
    finally:
        db.close()
    return {
        "status": "ok",
        "database": "connected" if db_ok else "unreachable — check DATABASE_URL",
    }
