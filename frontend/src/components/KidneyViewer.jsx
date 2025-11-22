import React, { Suspense } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, Stage } from "@react-three/drei";
import KidneyModel from "./KidneyModel";

export default function KidneyViewer({ mesh }) {
  return (
    <div style={{ width: "100%", height: "100vh" }}>
      <Canvas camera={{ position: [0, 0, 200], fov: 50 }}>
        <Suspense fallback={null}>
          <Stage intensity={0.5} environment="city" adjustCamera={true}>
            <KidneyModel mesh={mesh} />
          </Stage>
        </Suspense>

        <OrbitControls autoRotate autoRotateSpeed={1.0} enableZoom={true} />
      </Canvas>
    </div>
  );
}
