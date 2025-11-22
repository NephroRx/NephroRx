import React from "react";
import KidneyViewer from "../components/KidneyViewer";

export default function ResultsPage({ result }) {
  if (!result) return <p>No data received.</p>;

  return (
    <div style={{ padding: "20px" }}>
      <h1>Kidney Analysis Results</h1>

      <h2>Kidney Volume</h2>
      <p>{result.volume_cm3.toFixed(2)} cm³</p>

      <h2>3D Kidney Model</h2>
      <KidneyViewer mesh={result.mesh} />
    </div>
  );
}
