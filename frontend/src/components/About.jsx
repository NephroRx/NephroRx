import React, { useState } from 'react';

export default function AboutButton() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <style>{`
        .about-button-container {
          position: fixed;
          top: 2rem;
          left: 2rem;
          z-index: 50;
        }

        .about-button {
          background-color: rgba(139, 116, 98, 0.1);
          border: 1px solid rgba(139, 116, 98, 0.3);
          border-radius: 9999px;
          color: #8B7462;
          padding: 0.75rem 1.5rem;
          font-size: 0.875rem;
          font-weight: 300;
          letter-spacing: 0.1em;
          text-transform: uppercase;
          cursor: pointer;
          transition: all 0.3s;
          backdrop-filter: blur(10px);
        }

        .about-button:hover {
          background-color: rgba(139, 116, 98, 0.2);
          border-color: rgba(139, 116, 98, 0.5);
        }

        .popup-overlay {
          position: fixed;
          inset: 0;
          background-color: rgba(0, 0, 0, 0.7);
          display: flex;
          align-items: center;
          justify-content: center;
          z-index: 100;
          backdrop-filter: blur(5px);
        }

        .popup-content {
          background-color: rgba(26, 26, 26, 0.95);
          border: 1px solid rgba(139, 116, 98, 0.3);
          border-radius: 0;
          padding: 3rem;
          max-width: 600px;
          width: 90%;
          position: relative;
        }

        .popup-header {
          font-size: 2rem;
          font-weight: 300;
          color: #8B7462;
          margin-bottom: 1.5rem;
          letter-spacing: 0.05em;
        }

        .popup-text {
          color: #a1a1aa;
          font-size: 1rem;
          line-height: 1.6;
          font-weight: 300;
          margin-bottom: 1rem;
        }

        .popup-close {
          background-color: rgba(139, 116, 98, 0.1);
          border: 1px solid rgba(139, 116, 98, 0.3);
          border-radius: 9999px;
          color: #8B7462;
          padding: 0.75rem 2rem;
          font-size: 0.875rem;
          font-weight: 300;
          letter-spacing: 0.1em;
          text-transform: uppercase;
          cursor: pointer;
          transition: all 0.3s;
          margin-top: 1.5rem;
        }

        .popup-close:hover {
          background-color: rgba(139, 116, 98, 0.2);
          border-color: rgba(139, 116, 98, 0.5);
        }
      `}</style>

      <div className="about-button-container">
        <button className="about-button" onClick={() => setIsOpen(true)}>
          About
        </button>
      </div>

      {isOpen && (
        <div className="popup-overlay" onClick={() => setIsOpen(false)}>
          <div className="popup-content" onClick={(e) => e.stopPropagation()}>
            <h2 className="popup-header">About NephroRX</h2>
            <p className="popup-text">
              NephroRx is an advanced AI-powered medical imaging platform specifically designed for nephrology and oncology applications. 
              We convert kidney MRI scans into precise 3D volumetric reconstructions to enable smarter, data-driven medication dosing decisions.
            </p>
            <p className="popup-text">
              This tool is intended for research and educational purposes only and should be used under the guidance of qualified medical professionals.
            </p>
            <button className="popup-close" onClick={() => setIsOpen(false)}>
              Close
            </button>
          </div>
        </div>
      )}
    </>
  );
}