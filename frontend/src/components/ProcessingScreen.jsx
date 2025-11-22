import React, { useState, useEffect } from 'react';
import './ProcessingScreen.css';

const ProcessingScreen = ({ onComplete }) => {
  const [progress, setProgress] = useState(0);
  const [currentStage, setCurrentStage] = useState(0);

  const stages = [
    { name: 'Initializing Analysis Pipeline', duration: 1000 },
    { name: 'Loading Medical Image Data', duration: 1200 },
    { name: 'Preprocessing NIfTI/DICOM Files', duration: 1500 },
    { name: 'Constructing 3D Volumetric Model', duration: 1800 },
    { name: 'Identifying Kidney Structures', duration: 1400 },
    { name: 'Detecting Tumor Regions', duration: 1600 },
    { name: 'Calculating GFR from Creatinine', duration: 1000 },
    { name: 'Analyzing Kidney Function', duration: 1200 },
    { name: 'Computing Dosage Recommendations', duration: 1000 },
    { name: 'Finalizing Results', duration: 800 }
  ];

  useEffect(() => {
    let timer;
    let stageTimer;
    const totalDuration = stages.reduce((sum, stage) => sum + stage.duration, 0);
    let elapsedTime = 0;

    const updateProgress = () => {
      elapsedTime += 50;
      const newProgress = Math.min((elapsedTime / totalDuration) * 100, 100);
      setProgress(newProgress);

      // Update current stage
      let cumulativeTime = 0;
      for (let i = 0; i < stages.length; i++) {
        cumulativeTime += stages[i].duration;
        if (elapsedTime < cumulativeTime) {
          setCurrentStage(i);
          break;
        }
      }

      if (newProgress >= 100) {
        setTimeout(() => onComplete(), 500);
      }
    };

    timer = setInterval(updateProgress, 50);

    return () => {
      clearInterval(timer);
      if (stageTimer) clearTimeout(stageTimer);
    };
  }, [onComplete]);

  return (
    <div className="processing-screen">
      <div className="grid-background"></div>
      
      <div className="processing-container">
        <div className="processing-header">
          <div className="scan-animation">
            <div className="scan-line"></div>
            <div className="kidney-outline">
              <div className="kidney-left"></div>
              <div className="kidney-right"></div>
            </div>
          </div>
          <h1 className="processing-title">Analyzing Medical Data</h1>
        </div>

        <div className="processing-stages">
          {stages.map((stage, index) => (
            <div 
              key={index} 
              className={`stage-item ${index <= currentStage ? 'active' : ''} ${index < currentStage ? 'completed' : ''}`}
            >
              <div className="stage-indicator">
                {index < currentStage ? '✓' : index === currentStage ? '⟳' : '○'}
              </div>
              <span className="stage-name">{stage.name}</span>
              {index === currentStage && <span className="stage-spinner"></span>}
            </div>
          ))}
        </div>

        <div className="progress-section">
          <div className="progress-bar-container">
            <div className="progress-bar" style={{ width: `${progress}%` }}>
              <div className="progress-glow"></div>
            </div>
          </div>
          <div className="progress-text">{Math.round(progress)}% Complete</div>
        </div>

        <div className="processing-stats">
          <div className="stat-item">
            <div className="stat-value">{currentStage + 1}/{stages.length}</div>
            <div className="stat-label">Processing Stage</div>
          </div>
          <div className="stat-item">
            <div className="stat-value">{Math.round((10000 - (progress * 100)))}</div>
            <div className="stat-label">Data Points Analyzed</div>
          </div>
          <div className="stat-item">
            <div className="stat-value">{(10 - (progress / 10)).toFixed(1)}s</div>
            <div className="stat-label">Est. Time Remaining</div>
          </div>
        </div>

        <div className="technical-readout">
          <div className="readout-line">» Neural network inference: Active</div>
          <div className="readout-line">» GPU acceleration: Enabled</div>
          <div className="readout-line">» Image resolution: 512x512x256 voxels</div>
          <div className="readout-line">» Segmentation confidence: {(85 + progress / 10).toFixed(1)}%</div>
        </div>
      </div>
    </div>
  );
};

export default ProcessingScreen;
