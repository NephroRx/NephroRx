import React from "react";
import KidneyViewer from "../components/KidneyViewer";
import { Activity, ArrowLeft, FileText, Pill, Activity as ActivityIcon } from "lucide-react";
import { useLocation, useNavigate } from "react-router-dom";

export default function ResultsPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const result = location.state?.result;

  if (!result) return <div className="min-h-screen bg-[#121212] text-white flex items-center justify-center">No data received.</div>;

  return (
    <div className="min-h-screen bg-[#121212] text-white relative overflow-hidden font-sans">
      {/* Background / 3D Viewer Area */}
      <div className="absolute inset-0 z-0">
         <KidneyViewer mesh={result.mesh} />
      </div>

      {/* Overlay Content - Top Left */}
      <div className="relative z-10 p-8 md:p-12 max-w-md h-screen flex flex-col pointer-events-none">
        
        <button 
          onClick={() => navigate("/")} 
          className="pointer-events-auto self-start flex items-center gap-2 text-zinc-500 hover:text-[#8B7462] transition-colors mb-8 text-xs uppercase tracking-widest group"
        >
          <ArrowLeft size={14} className="group-hover:-translate-x-1 transition-transform" /> Back to Analysis
        </button>

        <div className="pointer-events-auto bg-[#1a1a1a]/60 backdrop-blur-xl border border-white/5 p-8 rounded-3xl shadow-2xl animate-fade-in-up">
          <div className="flex items-center gap-3 mb-8 border-b border-white/5 pb-6">
             <div className="p-2 bg-[#8B7462]/10 rounded-lg">
                <Activity className="text-[#8B7462]" size={20} />
             </div>
             <div>
                <h1 className="text-lg font-light tracking-wide text-zinc-100">Analysis Report</h1>
                <p className="text-[10px] text-zinc-500 uppercase tracking-widest">AI-Generated Assessment</p>
             </div>
          </div>

          <div className="space-y-8">
            {/* Volume Section */}
            <div>
              <p className="text-xs text-zinc-500 uppercase tracking-widest mb-2 flex items-center gap-2">
                <FileText size={12} /> Kidney Volume
              </p>
              <div className="flex items-baseline gap-2">
                <span className="text-6xl font-extralight text-white tracking-tighter">
                  {result.volume_cm3 ? result.volume_cm3.toFixed(1) : "0.0"}
                </span>
                <span className="text-zinc-500 font-light text-lg">cm³</span>
              </div>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-2 gap-4 bg-black/20 p-4 rounded-2xl border border-white/5">
               <div>
                  <p className="text-[10px] text-zinc-500 uppercase tracking-widest mb-1">Est. GFR</p>
                  <p className="text-2xl font-light text-zinc-200">{result.gfr_final ? result.gfr_final.toFixed(1) : "0.0"}</p>
                  <p className="text-[10px] text-zinc-600">mL/min/1.73m²</p>
               </div>
               <div>
                  <p className="text-[10px] text-zinc-500 uppercase tracking-widest mb-1">Creatinine</p>
                  <p className="text-2xl font-light text-zinc-200">{result.creatinine || "0.0"}</p>
                  <p className="text-[10px] text-zinc-600">mg/dL</p>
               </div>
            </div>

            {/* Recommendation */}
            <div>
               <p className="text-xs text-zinc-500 uppercase tracking-widest mb-3 flex items-center gap-2">
                  <Pill size={12} /> Recommended Dose
               </p>
               <div className="bg-gradient-to-r from-[#8B7462]/20 to-transparent border-l-2 border-[#8B7462] p-4 rounded-r-lg">
                  <p className="text-3xl text-[#e0cfc2] font-light tracking-tight">
                    {result.dose_mg ? result.dose_mg.toFixed(0) : "0"} <span className="text-lg text-[#8B7462]/70">mg</span>
                  </p>
                  <p className="text-[10px] text-[#8B7462]/70 mt-1">Adjusted for renal function</p>
               </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
