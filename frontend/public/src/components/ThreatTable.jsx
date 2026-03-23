export default function ThreatTable({ threats }) {
  // Hide the table entirely if there are no threats
  if (!threats || threats.length === 0) return null;

  // Helper function to color-code the severity badges
  const getBadgeColor = (severity) => {
    switch (severity) {
      case 'CRITICAL': return 'bg-red-500/10 text-red-400 border-red-500/50';
      case 'HIGH': return 'bg-orange-500/10 text-orange-400 border-orange-500/50';
      case 'MEDIUM': return 'bg-yellow-500/10 text-yellow-400 border-yellow-500/50';
      default: return 'bg-slate-500/10 text-slate-400 border-slate-500/50';
    }
  };

  return (
    <div className="bg-[#1e293b] rounded-xl border border-slate-700 shadow-xl overflow-hidden mt-8">
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-800 text-slate-300 text-xs uppercase tracking-wider">
              <th className="p-5 font-semibold border-b border-slate-700">Severity</th>
              <th className="p-5 font-semibold border-b border-slate-700">Rule Violation</th>
              <th className="p-5 font-semibold border-b border-slate-700">Description</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-700/50">
            {threats.map((t, i) => (
              <tr key={i} className="hover:bg-slate-800/50 transition-colors duration-150">
                {/* Severity Badge Column */}
                <td className="p-5 whitespace-nowrap align-top">
                  <span className={`px-3 py-1 rounded-full text-xs font-bold border ${getBadgeColor(t.Severity)}`}>
                    {t.Severity}
                  </span>
                </td>
                
                {/* Rule Column */}
                <td className="p-5 font-medium text-slate-200 align-top">{t.Rule}</td>
                
                {/* Description & AI Explanation Column */}
                <td className="p-5 text-slate-400 text-sm align-top">
                  <p className="mb-3">{t.Description}</p>
                  
                  {/* The New AI Explanation Block */}
                  {t.Explanation && (
                    <div className="p-4 bg-blue-900/10 border border-blue-500/20 rounded-lg text-blue-300 font-mono text-xs shadow-inner mt-2">
                      <span className="font-bold text-blue-400 uppercase tracking-wider block mb-1">↳ AI Analysis:</span> 
                      {t.Explanation}
                    </div>
                  )}
                  
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}