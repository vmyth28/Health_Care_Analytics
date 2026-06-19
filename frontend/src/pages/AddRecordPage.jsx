import { useState } from "react";
import { addRecord } from "../services/api";

const initialForm = {
  patient_id: "",
  age: "",
  gender: "Male",
  disease: "Diabetes",
  hospital: "Apollo Hospital",
  admission_date: "2025-06-01",
  discharge_date: "2025-06-05",
  claim_amount: "",
  claim_status: "Approved",
  city: "Noida",
};

function AddRecordPage() {
  const [form, setForm] = useState(initialForm);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const update = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const submit = async (e) => {
    e.preventDefault();
    setMessage("");
    setError("");
    try {
      const payload = {
        ...form,
        age: Number(form.age),
        claim_amount: Number(form.claim_amount),
      };
      const res = await addRecord(payload);
      setMessage(`Record added successfully with ID ${res.id}`);
      setForm(initialForm);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to add record");
    }
  };

  return (
    <div className="section-card">
      <h1>Add Manual Record</h1>
      <form className="form-grid" onSubmit={submit}>
        <input name="patient_id" placeholder="Patient ID" value={form.patient_id} onChange={update} required />
        <input name="age" type="number" placeholder="Age" value={form.age} onChange={update} required />
        <select name="gender" value={form.gender} onChange={update}><option>Male</option><option>Female</option><option>Other</option></select>
        <input name="disease" placeholder="Disease" value={form.disease} onChange={update} required />
        <input name="hospital" placeholder="Hospital" value={form.hospital} onChange={update} required />
        <input name="city" placeholder="City" value={form.city} onChange={update} required />
        <input name="admission_date" type="date" value={form.admission_date} onChange={update} required />
        <input name="discharge_date" type="date" value={form.discharge_date} onChange={update} required />
        <input name="claim_amount" type="number" placeholder="Claim Amount" value={form.claim_amount} onChange={update} required />
        <select name="claim_status" value={form.claim_status} onChange={update}><option>Approved</option><option>Rejected</option><option>Pending</option></select>
        <button type="submit">Add Record</button>
      </form>
      {message && <p className="success">{message}</p>}
      {error && <p className="error">{String(error)}</p>}
    </div>
  );
}

export default AddRecordPage;
