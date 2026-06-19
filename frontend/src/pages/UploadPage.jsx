import { useState } from "react";
import { uploadCsv } from "../services/api";

function UploadPage() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError("Please select a CSV file.");
      return;
    }
    setLoading(true);
    setError("");
    setResult(null);
    const formData = new FormData();
    formData.append("file", file);
    try {
      setResult(await uploadCsv(formData));
    } catch (err) {
      setError(err.response?.data?.detail || "Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="section-card small-card">
      <h1>Upload CSV</h1>
      <p>Use sample file from: backend/sample_data/healthcare_sample.csv</p>
      <form onSubmit={handleSubmit} className="form">
        <input type="file" accept=".csv" onChange={(e) => setFile(e.target.files[0])} />
        <button type="submit" disabled={loading}>{loading ? "Uploading..." : "Upload"}</button>
      </form>
      {error && <p className="error">{error}</p>}
      {result && (
        <div className="success-box">
          <h3>{result.message}</h3>
          <p>Total: {result.total_records}</p>
          <p>Valid: {result.valid_records}</p>
          <p>Invalid: {result.invalid_records}</p>
          <p>Inserted: {result.rows_inserted}</p>
        </div>
      )}
    </div>
  );
}

export default UploadPage;
