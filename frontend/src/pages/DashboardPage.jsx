import { useEffect, useState } from "react";
import SummaryCard from "../components/SummaryCard";
import { getSummary, getRecentRecords, testBackend } from "../services/api";

function DashboardPage() {
  const [summary, setSummary] = useState(null);
  const [recent, setRecent] = useState([]);
  const [connection, setConnection] = useState("Checking...");

  const loadData = async () => {
    try {
      await testBackend();
      setConnection("Connected ✅");
      setSummary(await getSummary());
      setRecent(await getRecentRecords());
    } catch (error) {
      setConnection("Backend not reachable ❌");
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 5000); // polling, no websocket
    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <div className="page-header">
        <h1>Dashboard</h1>
        <p>Status: {connection}</p>
      </div>

      {!summary ? <p>Loading dashboard...</p> : (
        <div className="grid cards-grid">
          <SummaryCard title="Total Patients" value={summary.total_patients} />
          <SummaryCard title="Total Claim Amount" value={`₹${summary.total_claim_amount.toLocaleString()}`} />
          <SummaryCard title="Average Claim Amount" value={`₹${summary.average_claim_amount.toLocaleString()}`} />
          <SummaryCard title="Most Common Disease" value={summary.most_common_disease} />
          <SummaryCard title="Top Hospital" value={summary.top_hospital} />
          <SummaryCard title="Approved Claims" value={summary.approved_claims} />
          <SummaryCard title="Rejected Claims" value={summary.rejected_claims} />
          <SummaryCard title="Pending Claims" value={summary.pending_claims} />
        </div>
      )}

      <div className="section-card">
        <h2>Recent Records</h2>
        {recent.length === 0 ? <p>No recent records yet. Upload CSV or add a record.</p> : (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Patient ID</th><th>Disease</th><th>Hospital</th><th>Claim</th><th>Status</th>
                </tr>
              </thead>
              <tbody>
                {recent.map((r) => (
                  <tr key={r.id}>
                    <td>{r.patient_id}</td>
                    <td>{r.disease}</td>
                    <td>{r.hospital}</td>
                    <td>₹{r.claim_amount}</td>
                    <td>{r.claim_status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default DashboardPage;
