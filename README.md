# Healthcare Data Analytics and Prediction Dashboard

A complete full-stack healthcare analytics project using:

- **Backend:** Python, FastAPI, Pandas, SQLAlchemy, Scikit-learn
- **Frontend:** React, Vite, Axios, Recharts, normal CSS
- **Database:** PostgreSQL supported; SQLite fallback included for easy first run
- **Features:** CSV upload, manual record entry, dashboard analytics, charts, auto insights, polling-based updates, ML claim amount prediction

> This project uses dummy/sample healthcare data only. Do not upload real patient data.

---

## Project Structure

```text
healthcare-analytics-dashboard/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── routes/
│   │   └── services/
│   ├── sample_data/
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── package.json
    ├── vite.config.js
    └── src/
```

---

## Quick Run Option 1: Run Immediately With SQLite

This is the easiest way to check that the project works.

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs at:

```text
http://localhost:8000
```

Open API docs:

```text
http://localhost:8000/docs
```

### Frontend

Open a new terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

---

## Option 2: Use PostgreSQL

1. Install PostgreSQL.
2. Create a database named:

```text
healthcare_db
```

3. In `backend`, create `.env` by copying `.env.example`:

```bash
copy .env.example .env
```

4. Edit `.env`:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/healthcare_db
```

5. Run backend again:

```bash
uvicorn app.main:app --reload
```

---

## Main Features

### 1. CSV Upload
Upload healthcare CSV data. Backend cleans data and stores it in the database.

### 2. Manual Record Entry
Add one healthcare record manually from React form.

### 3. Dashboard Summary
Shows:

- Total records
- Total claim amount
- Average claim amount
- Most common disease
- Top hospital
- Approved/rejected/pending claims

### 4. Analytics Charts
Uses Recharts for:

- Patient trends
- Disease distribution
- Hospital performance
- Claim status distribution

### 5. Auto Insights
Backend generates business-style insights from latest data.

### 6. ML Claim Amount Prediction
Uses RandomForestRegressor to predict claim amount based on:

- Age
- Gender
- Disease
- Hospital
- City
- Length of stay

### 7. Polling-Based Auto Update
Dashboard refreshes every 5 seconds. No WebSocket is used.

---

## Sample CSV

Use this file:

```text
backend/sample_data/healthcare_sample.csv
```

Upload it from the frontend Upload page.

---

## Recommended Run Order

1. Start backend.
2. Start frontend.
3. Open frontend.
4. Upload sample CSV.
5. Open Dashboard and Analytics.
6. Add a manual record.
7. Train ML model.
8. Try prediction.

---

## Important Notes

- The project will create database tables automatically.
- If `.env` is missing, backend uses SQLite automatically.
- For portfolio/interview, use PostgreSQL.
- Do not push real `.env` to GitHub.
