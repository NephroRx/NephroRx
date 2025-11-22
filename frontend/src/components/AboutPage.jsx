import React from 'react';
import './AboutPage.css';

const AboutPage = ({ onClose }) => {
  return (
    <div className="about-overlay">
      <div className="grid-background"></div>
      <button className="close-button" onClick={onClose}>×</button>
      
      <div className="about-container">
        <h1 className="about-title">About NephroRx</h1>
        
        <div className="about-content">
          <section className="about-section">
            <h2>Our Mission</h2>
            <p>
              NephroRx is an advanced AI-powered medical imaging platform specifically designed for nephrology and oncology applications. 
              We convert kidney MRI scans into precise 3D volumetric reconstructions to enable smarter, data-driven medication dosing decisions.
            </p>
          </section>

          <section className="about-section">
            <h2>Treatment Approach & Drug Dosing</h2>
            <p>
              Cancer treatment follows a tiered approach based on severity and stage:
            </p>
            <ul>
              <li><strong>Early Stage:</strong> Targeted radiotherapy to eliminate tumor cells with minimal damage to healthy tissue</li>
              <li><strong>Progressive Stage:</strong> Combination therapy with adjusted dosing based on kidney function</li>
              <li><strong>Advanced Stage:</strong> Chemotherapy as a comprehensive approach - targeting all rapidly dividing cells with the hope that tumor cells are eliminated alongside some healthy cells</li>
            </ul>
            <p className="highlight-text">
              Chemotherapy is used as a last-resort treatment option when other methods have proven insufficient.
            </p>
          </section>

          <section className="about-section">
            <h2>Creatinine-Based Dosing Calculations</h2>
            <p>
              Our platform uses serum creatinine levels from bloodwork to calculate precise medication dosages. Here's how it works:
            </p>
            
            <div className="calculation-box">
              <h3>Glomerular Filtration Rate (GFR) Calculation</h3>
              <p>We use the CKD-EPI equation to estimate kidney function:</p>
              <code>
                eGFR = 141 × min(SCr/κ, 1)^α × max(SCr/κ, 1)^-1.209 × 0.993^Age
              </code>
              <p className="small-text">Where SCr = serum creatinine, κ and α are constants based on sex</p>
            </div>

            <div className="calculation-box">
              <h3>Drug Dosage Adjustment</h3>
              <p>Medication dosage is adjusted as a percentage based on kidney function:</p>
              <ul>
                <li><strong>GFR ≥90 mL/min:</strong> 100% of standard dose (Normal kidney function)</li>
                <li><strong>GFR 60-89:</strong> 75-100% of standard dose (Mildly decreased function)</li>
                <li><strong>GFR 45-59:</strong> 50-75% of standard dose (Mild-moderate decrease)</li>
                <li><strong>GFR 30-44:</strong> 25-50% of standard dose (Moderate-severe decrease)</li>
                <li><strong>GFR 15-29:</strong> 10-25% of standard dose (Severe decrease)</li>
                <li><strong>GFR &lt;15:</strong> Dialysis-dependent dosing (Kidney failure)</li>
              </ul>
            </div>
          </section>

          <section className="about-section">
            <h2>Cancer Stage Analysis</h2>
            <p>
              Our system provides in-depth analysis for patients at various cancer stages:
            </p>
            
            <div className="stage-info">
              <h3>Late-Stage Cancer (Stage III-IV)</h3>
              <p>For patients with advanced kidney cancer, our analysis includes:</p>
              <ul>
                <li><strong>Tumor Volume Quantification:</strong> Precise 3D measurements of tumor size and growth patterns</li>
                <li><strong>Kidney Function Assessment:</strong> Real-time evaluation of remaining kidney capacity</li>
                <li><strong>Vascular Involvement:</strong> Analysis of blood vessel invasion and metastatic spread</li>
                <li><strong>Treatment Response Tracking:</strong> Monitoring tumor shrinkage or growth during therapy</li>
                <li><strong>Personalized Dosing:</strong> Adjusting chemotherapy doses based on declining kidney function while maximizing efficacy</li>
              </ul>
              
              <p className="warning-text">
                In late-stage cancer, kidney function often deteriorates due to both tumor burden and treatment effects. 
                Our platform continuously recalculates safe drug dosages to prevent toxicity while maintaining therapeutic effectiveness.
              </p>
            </div>
          </section>

          <section className="about-section">
            <h2>3D Volumetric Reconstruction</h2>
            <p>
              Our advanced imaging algorithms process NIfTI and DICOM files to create detailed 3D models of kidney structures, 
              enabling precise tumor localization and volume calculations essential for treatment planning.
            </p>
          </section>

          <section className="about-section">
            <h2>Clinical Accuracy</h2>
            <p>
              NephroRx combines machine learning with established clinical guidelines to ensure accurate, 
              evidence-based dosing recommendations. All calculations follow FDA-approved protocols and are designed 
              to assist healthcare providers in making informed treatment decisions.
            </p>
          </section>
        </div>
      </div>
    </div>
  );
};

export default AboutPage;
