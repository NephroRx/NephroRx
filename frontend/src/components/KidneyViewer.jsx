import React, { Suspense } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, Stage } from "@react-three/drei";
import KidneyModel from "./KidneyModel";

export default function KidneyViewer({ mesh }) {
  return (
    <div style={{ width: "100%", height: "500px", background: "black" }}>
      <Canvas camera={{ position: [0, 0, 5] }}>
        <Suspense fallback={null}>
          <Stage intensity={0.5} environment="city">
            <KidneyModel mesh={mesh} />
          </Stage>
        </Suspense>

        <OrbitControls />
      </Canvas>
    </div>
  );
}
