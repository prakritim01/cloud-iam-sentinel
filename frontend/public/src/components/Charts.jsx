import Plot from "react-plotly.js";

export default function Charts({ threats }) {
  if (!threats || threats.length === 0) return null;

  const counts = {};
  threats.forEach(t => {
    counts[t.Severity] = (counts[t.Severity] || 0) + 1;
  });

  const colorMap = {
    'CRITICAL': '#ef4444', 
    'HIGH': '#f97316',     
    'MEDIUM': '#eab308'    
  };
  const markerColors = Object.keys(counts).map(severity => colorMap[severity] || '#64748b');

  return (
    <Plot
      data={[
        {
          values: Object.values(counts),
          labels: Object.keys(counts),
          type: "pie",
          hole: 0.75,
          marker: { colors: markerColors },
          textinfo: "none", 
          hoverinfo: "label+value"
        }
      ]}
      layout={{
        height: 250,
        width: 300,
        margin: { t: 10, b: 10, l: 10, r: 10 },
        showlegend: true,
        legend: { font: { color: "#cbd5e1" } },
        paper_bgcolor: "rgba(0,0,0,0)", // Makes background transparent
        plot_bgcolor: "rgba(0,0,0,0)",  // Makes plot area transparent
      }}
      config={{ displayModeBar: false }}
    />
  );
}