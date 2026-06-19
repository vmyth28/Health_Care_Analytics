import { Routes, Route, NavLink } from "react-router-dom";
import DashboardPage from "./pages/DashboardPage";
import UploadPage from "./pages/UploadPage";
import AddRecordPage from "./pages/AddRecordPage";
import AnalyticsPage from "./pages/AnalyticsPage";
import InsightsPage from "./pages/InsightsPage";
import PredictionPage from "./pages/PredictionPage";

function App() {
  return (
    <div>
      <nav className="navbar">
        <div className="brand">Healthcare Analytics</div>
        <div className="nav-links">
          <NavLink to="/">Dashboard</NavLink>
          <NavLink to="/upload">Upload CSV</NavLink>
          <NavLink to="/add-record">Add Record</NavLink>
          <NavLink to="/analytics">Analytics</NavLink>
          <NavLink to="/insights">Insights</NavLink>
          <NavLink to="/prediction">Prediction</NavLink>
        </div>
      </nav>

      <main className="main">
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/upload" element={<UploadPage />} />
          <Route path="/add-record" element={<AddRecordPage />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
          <Route path="/insights" element={<InsightsPage />} />
          <Route path="/prediction" element={<PredictionPage />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
