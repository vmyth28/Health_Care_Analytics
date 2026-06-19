from pathlib import Path
import joblib
import pandas as pd
from sqlalchemy.orm import Session
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from app.services.analytics_service import records_to_dataframe

MODEL_PATH = Path(__file__).resolve().parent.parent / "ml_models" / "claim_model.pkl"

FEATURES = ["age", "gender", "disease", "hospital", "city", "length_of_stay"]
TARGET = "claim_amount"


def train_claim_model(db: Session):
    df = records_to_dataframe(db)
    if df.empty or len(df) < 5:
        return {
            "status": "error",
            "message": "At least 5 records are required to train the ML model.",
            "training_records": int(len(df)),
            "model_score": None,
        }

    df = df.dropna(subset=FEATURES + [TARGET])
    X = df[FEATURES]
    y = df[TARGET]

    categorical_features = ["gender", "disease", "hospital", "city"]
    numeric_features = ["age", "length_of_stay"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
            ("num", "passthrough", numeric_features),
        ]
    )

    model = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("regressor", RandomForestRegressor(n_estimators=100, random_state=42)),
    ])

    if len(df) >= 10:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        score = r2_score(y_test, predictions)
    else:
        model.fit(X, y)
        score = None

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    return {
        "status": "success",
        "message": "Model trained successfully.",
        "training_records": int(len(df)),
        "model_score": None if score is None else round(float(score), 4),
    }


def predict_claim_amount(payload):
    if not MODEL_PATH.exists():
        return {
            "status": "error",
            "message": "Model not trained yet. Please train the model first.",
            "predicted_claim_amount": None,
        }

    model = joblib.load(MODEL_PATH)
    length_of_stay = (payload.discharge_date - payload.admission_date).days
    input_df = pd.DataFrame([{
        "age": payload.age,
        "gender": payload.gender.strip().title(),
        "disease": payload.disease.strip(),
        "hospital": payload.hospital.strip(),
        "city": payload.city.strip(),
        "length_of_stay": max(length_of_stay, 0),
    }])

    prediction = model.predict(input_df)[0]
    return {
        "status": "success",
        "predicted_claim_amount": round(float(prediction), 2),
    }
