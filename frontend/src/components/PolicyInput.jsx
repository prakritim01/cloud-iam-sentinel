import { useState } from "react";

export default function PolicyInput({ onScan }) {
  const [policy, setPolicy] = useState("");

  return (
    <div>
      <textarea
        className="w-full h-60 p-4 bg-gray-800 rounded"
        value={policy}
        onChange={(e) => setPolicy(e.target.value)}
      />
      <button
        className="mt-4 px-6 py-2 bg-green-600 rounded"
        onClick={() => onScan(policy)}
      >
        Scan
      </button>
    </div>
  );
}