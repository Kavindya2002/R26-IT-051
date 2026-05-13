import React, { useRef, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera } from '@react-three/drei';
import * as THREE from 'three';

interface Props {
  activity: string;
  accel: { x: number; y: number; z: number };
}
interface Patient3DViewProps {
  activity: string;
  accel: { x: number; y: number; z: number }; // Accel 
}

interface ModelProps {
  activity: string;
  accel: { x: number; y: number; z: number };
  setTiltData: (data: { percentage: string; direction: string }) => void;
}




function RealPersonModel({ activity, accel, setTiltData }: ModelProps) {  // TypeScript -> Ref 
  const bodyRef = useRef<THREE.Group>(null);
  const leftLegRef = useRef<THREE.Group>(null);
  const rightLegRef = useRef<THREE.Group>(null);
  const leftArmRef = useRef<THREE.Group>(null);
  const rightArmRef = useRef<THREE.Group>(null);

useFrame((state) => {
  const { current: body } = bodyRef;
  const { current: lLeg } = leftLegRef;
  const { current: rLeg } = rightLegRef;
  const { current: lArm } = leftArmRef;
  const { current: rArm } = rightArmRef;

  if (!bodyRef.current) return;

    // anshaka calculate
    const tiltX = (accel.x / 9.8) * (Math.PI / 4); 
    
    // presentage calculate (max 45° = 100%)
    const tiltPercentage = Math.min(Math.abs((accel.x / 9.8) * 100), 100).toFixed(0);
    
    // side decide
    const direction = accel.x > 0.1 ? "Right" : accel.x < -0.1 ? "Left" : "Straight";

    // UI -\> data
    setTiltData({ percentage: tiltPercentage, direction: direction });

    // Model rotate
    bodyRef.current.rotation.z = -tiltX;

  // check all refs have
  if (!body || !lLeg || !rLeg || !lArm || !rArm) return;

  const time = state.clock.getElapsedTime();
  const currentAct = activity ? activity.toLowerCase() : "standing";

  // --- 1. Tilt & Fall Logic (everytime work) ---
  //const tiltSide = (accel.x / 9.8) * (Math.PI / 3);
  //const tiltFront = (accel.y / 9.8) * (Math.PI / 3);
/*
  if (accel.z < 6) {
    //  (Fall) show
    body.rotation.z = Math.PI / 2.5; 
    body.position.y = -0.8;
  } else {
    // (Tilt) show
    body.rotation.z = -tiltSide;
    body.rotation.x = tiltFront;}
    */
 
 // --- 1. Tilt & Fall Logic ---
const tiltSide = (accel.x / 9.8) * (Math.PI / 3);
const tiltFront = (accel.y / 9.8) * (Math.PI / 3);

// 'standing' හෝ 'walking' වෙලාවට වැටිලා වගේ පේන්න එපා
if (accel.z < 6 && currentAct !== "standing" && currentAct !== "walking") {
    body.rotation.z = Math.PI / 2.5; 
    body.position.y = -0.8;
} else {
    // සාමාන්‍ය අවස්ථාවලදී ඇලවීම (Tilt) පමණක් පෙන්වන්න
    body.rotation.z = -tiltSide;
    body.rotation.x = tiltFront;
    body.position.y = 0; // ආපහු කෙලින් කරන්න
}
   
  

  // --- 2. Activity Animations (Walking/Sitting/Standing) ---
  if (currentAct === "walking") {
    // body go up and down
    body.position.y = Math.sin(time * 10) * 0.05;
    
    // hands,legs wanima
    const swing = Math.sin(time * 10) * 0.6;
    lLeg.rotation.x = swing;
    rLeg.rotation.x = -swing;
    lArm.rotation.x = -swing * 0.5;
    rArm.rotation.x = swing * 0.5;
  } 
  else if (currentAct === "sitting") {
    body.position.y = -0.5;
    lLeg.rotation.x = -Math.PI / 2.5;
    rLeg.rotation.x = -Math.PI / 2.5;
    lArm.rotation.x = 0;
    rArm.rotation.x = 0;
  } 
  else {
    // Standing: all normal
    if (accel.z >= 6) body.position.y = 0;
    lLeg.rotation.x = 0;
    rLeg.rotation.x = 0;
    lArm.rotation.x = 0;
    rArm.rotation.x = 0;
  }
});

  return (
    <group ref={bodyRef}>
      {/* head */}
      <mesh position={[0, 1.6, 0]}>
        <sphereGeometry args={[0.15, 32, 32]} />
        <meshStandardMaterial color="#ffdbac" />
      </mesh>
      {/* body */}
      <mesh position={[0, 1, 0]}>
        <boxGeometry args={[0.4, 0.7, 0.2]} />
        <meshStandardMaterial color="#0055ff" />
      </mesh>
      {/* right hand */}
      <group ref={rightArmRef} position={[0.25, 1.3, 0]}>
        <mesh position={[0, -0.25, 0]}>
          <capsuleGeometry args={[0.05, 0.5, 4, 8]} />
          <meshStandardMaterial color="#ffdbac" />
        </mesh>
      </group>
      {/* left hand */}
      <group ref={leftArmRef} position={[-0.25, 1.3, 0]}>
        <mesh position={[0, -0.25, 0]}>
          <capsuleGeometry args={[0.05, 0.5, 4, 8]} />
          <meshStandardMaterial color="#ffdbac" />
        </mesh>
      </group>
      {/* right leg */}
      <group ref={rightLegRef} position={[0.15, 0.65, 0]}>
        <mesh position={[0, -0.35, 0]}>
          <capsuleGeometry args={[0.07, 0.7, 4, 8]} />
          <meshStandardMaterial color="#ffdbac" />
        </mesh>
      </group>
      {/* lef leg*/}
      <group ref={leftLegRef} position={[-0.15, 0.65, 0]}>
        <mesh position={[0, -0.35, 0]}>
          <capsuleGeometry args={[0.07, 0.7, 4, 8]} />
          <meshStandardMaterial color="#ffdbac" />
        </mesh>
      </group>
    </group>
  );
}

export default function Patient3DView({ activity, accel }: Props) {
  const [tiltData, setTiltData] = useState({ percentage: "0", direction: "සෘජු" });

  return (
    //  container - relative position 
    <div style={{ position: 'relative', width: '100%', height: '350px', background: '#0a0a0a', borderRadius: '15px', overflow: 'hidden', marginTop:'-20px'}}>
      
      {/* Tilt Display Overlay -  above Canvas */}
      <div style={{
        position: 'absolute', top: '40px', left: '15px', zIndex: 10,
        background: 'rgba(0,0,0,0.7)', padding: '12px', borderRadius: '8px',
        border: '1px solid #444', color: '#fff', fontSize: '14px', pointerEvents: 'none'
      }}>
        <div style={{ marginBottom: '4px' }}>Body Tilt: <strong style={{ color: '#00d2ff' }}>{tiltData.percentage}%</strong></div>
        <div style={{ color: tiltData.direction === "Straight" ? "#28c941" : "#ffbd2e", fontWeight: 'bold' }}>
          {tiltData.direction === "Right" && "➡ "}
          {tiltData.direction === "Left" && "⬅ "}
          {tiltData.direction}
        </div>
      </div>

      {/* 3D Canvas */}
      <Canvas shadows camera={{ position: [2, 2, 4], fov: 50 }}>
        <ambientLight intensity={0.7} />
        <pointLight position={[10, 10, 10]} intensity={1.5} />
        
        {/* : setTiltData  */}
        <RealPersonModel 
          activity={activity} 
          accel={accel} 
          setTiltData={setTiltData} 
        />
        
        <gridHelper args={[10, 10, '#444', '#222']} />
        <OrbitControls enablePan={false} />
      </Canvas>
    </div>
  );
}