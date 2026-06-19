import { useEffect, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell, Legend } from "recharts";
import { getPatientTrends, getDiseaseDistribution, getHospitalPerformance, getClaimStatus } from "../services/api";

const COLORS = ["#2563eb", "#16a34a", "#f97316", "#9333ea", "#dc2626", "#0891b2"];

function AnalyticsPage() {
  const [trends, setTrends] = useState([]);
  const [diseases, setDiseases] = useState([]);
  const [hospitals, setHospitals] = useState([]);
  const [statuses, setStatuses] = useState([]);

  const load = async () => {
    setTrends(await getPatientTrends());
    setDiseases(await getDiseaseDistribution());
    setHospitals(await getHospitalPerformance());
    setStatuses(await getClaimStatus());
  };

  useEffect(() => {
    load();
    const interval = setInterval(load, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <h1>Analytics</h1>
      <div className="charts-grid">
        <div className="section-card chart-card">
          <h2>Patient Trends</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={trends}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="patients" stroke="#2563eb" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="section-card chart-card">
          <h2>Disease Distribution</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie data={diseases} dataKey="count" nameKey="disease" outerRadius={95} label>
                {diseases.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="section-card chart-card">
          <h2>Hospital Performance</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={hospitals}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="hospital" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="patient_count" fill="#16a34a" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="section-card chart-card">
          <h2>Claim Status</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={statuses}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="status" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#f97316" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

export default AnalyticsPage;
