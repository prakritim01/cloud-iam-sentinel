import { useState } from "react";
import PolicyInput from "../components/PolicyInput";
import ScoreCard from "../components/ScoreCard";
import ThreatTable from "../components/ThreatTable";
import Charts from "../../components/Charts";
import { scanPolicy } from "../services/api";

export default function Dashboard() {
  const [data, setData] = useState(null);

  const handleScan = async (policy) => {
    const res = await scanPolicy(policy);
    setData(res);
  };

  return (
    <div className="p-6 bg-gray-900 min-h-screen text-white">
      <PolicyInput onScan={handleScan} />
      {data && (
        <>
          <ScoreCard score={data.score} />
          <Charts threats={data.threats} />
          <ThreatTable threats={data.threats} />
        </>
      )}
    </div>
  );
}