import { useEffect, useState } from "react";
import { getInsights } from "../services/api";

function InsightsPage() {
  const [insights, setInsights] = useState([]);

  useEffect(() => {
    const load = async () => setInsights((await getInsights()).insights);
    load();
    const interval = setInterval(load, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="section-card">
      <h1>Auto Generated Insights</h1>
      {insights.map((item, index) => (
        <div className="insight" key={index}>{index + 1}. {item}</div>
      ))}
    </div>
  );
}

export default InsightsPage;
