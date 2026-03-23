export default function ScoreCard({ score }) {
  return (
    <div className="mt-4 text-xl">
      Security Score: {score}/100
    </div>
  );
}