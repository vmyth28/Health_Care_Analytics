import { useState } from "react";
import { trainModel, predictClaim } from "../services/api";

const initialForm = {
  age: "",
  gender: "Male",
  disease: "Diabetes",
  hospital: "Apollo Hospital",
  admission_date: "2025-06-01",
  discharge_date: "2025-06-05",
  city: "Noida",
};

function PredictionPage() {
  const [form, setForm] = useState(initialForm);
  const [trainResult, setTrainResult] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState("");

  const update = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const train = async () => {
    setError("");
    setPrediction(null);
    try {
      setTrainResult(await trainModel());
    } catch {
      setError("Training failed");
    }
  };

  const predict = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const res = await predictClaim({ ...form, age: Number(form.age) });
      if (res.status === "error") setError(res.message);
      else setPrediction(res.predicted_claim_amount);
    } catch (err) {
      setError(err.response?.data?.detail || "Prediction failed");
    }
  };

  return (
    <div className="section-card">
      <h1>ML Claim Prediction</h1>
      <button onClick={train}>Train Model</button>
      {trainResult && <pre className="result-box">{JSON.stringify(trainResult, null, 2)}</pre>}

      <form className="form-grid" onSubmit={predict}>
        <input name="age" type="number" placeholder="Age" value={form.age} onChange={update} required />
        <select name="gender" value={form.gender} onChange={update}><option>Male</option><option>Female</option><option>Other</option></select>
        <input name="disease" placeholder="Disease" value={form.disease} onChange={update} required />
        <input name="hospital" placeholder="Hospital" value={form.hospital} onChange={update} required />
        <input name="city" placeholder="City" value={form.city} onChange={update} required />
        <input name="admission_date" type="date" value={form.admission_date} onChange={update} required />
        <input name="discharge_date" type="date" value={form.discharge_date} onChange={update} required />
        <button type="submit">Predict Claim</button>
      </form>
      {prediction && <h2 className="success">Predicted Claim Amount: ₹{prediction.toLocaleString()}</h2>}
      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default PredictionPage;
