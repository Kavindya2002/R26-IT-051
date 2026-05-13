import React from 'react'

interface Props {
  score: number
  patientName: string
  bed: string
}

function getRiskSettings(s: number, bed: string) {
  const lastFive = ['Bed 10', 'Bed 11', 'Bed 12', 'Bed 13', 'Bed 14'];
  const isHighSensitivity = lastFive.includes(bed);
  const criticalThreshold = isHighSensitivity ? 60 : 75;

  if (s >= criticalThreshold) return { label: 'CRITICAL', color: '#f85149' };
  if (s >= 50) return { label: 'HIGH RISK', color: '#000000' };
  if (s >= 25) return { label: 'WARNIING', color: '#d29922' };
  return { label: 'STABLE', color: '#3fb950' };
}

export default function LiveRiskMeter({ score, patientName, bed }: Props) {
  const settings = getRiskSettings(score, bed);
  const color = settings.color;
  const label = settings.label;
  const needle = score * 1.8; // 0 to 180 degrees
  const isHighSensitivity = ['Bed 10', 'Bed 11', 'Bed 12', 'Bed 13', 'Bed 14'].includes(bed);

  return (
    <div style={{ 
      background: '#0d1117', 
      padding: '25px', 
      borderRadius: '20px', 
      display: 'inline-flex', 
      flexDirection: 'column', 
      alignItems: 'center',
      fontFamily: 'sans-serif',
      border: '1px solid #30363d'
    }}>
      <div style={{ 
        fontSize: '14px', 
        color: '#8b949e', 
        letterSpacing: '3px', 
        textTransform: 'uppercase', 
        marginBottom: '25px',
        fontWeight: 600
      }}>
        LIVE RISK METER - 3D VIEW
      </div>

      <div style={{ position: 'relative', width: 280, height: 160 }}>
        <svg viewBox="0 0 260 150" width="280" height="160" style={{ overflow: 'visible' }}>
          {/* Background Track with Glow */}
          <path 
            d="M 30 130 A 100 100 0 0 1 230 130" 
            fill="none" 
            stroke="#21262d" 
            strokeWidth="12" 
            strokeLinecap="round" 
          />

          {/* Dynamic Arcs based on Sensitivity */}
          <g style={{ filter: 'drop-shadow(0px 0px 4px rgba(0,0,0,0.5))' }}>
            {/* STABLE */}
            <path d="M 30 130 A 100 100 0 0 1 80 47" fill="none" stroke="#3fb950" strokeWidth="12" strokeLinecap="butt" />
            {/* WARNING */}
            <path d="M 80 47 A 100 100 0 0 1 130 30" fill="none" stroke="#d29922" strokeWidth="12" strokeLinecap="butt" />
            {/* HIGH RISK / CRITICAL depends on sensitivity */}
            <path 
              d={isHighSensitivity ? "M 130 30 A 100 100 0 0 1 155 33" : "M 130 30 A 100 100 0 0 1 193 52"} 
              fill="none" stroke="#e06c00" strokeWidth="12" 
            />
            <path 
              d={isHighSensitivity ? "M 155 33 A 100 100 0 0 1 230 130" : "M 193 52 A 100 100 0 0 1 230 130"} 
              fill="none" stroke="#f85149" strokeWidth="12" strokeLinecap="round"
            />
          </g>

          {/* Scale Markers */}
          {[0, 45, 90, 135, 180].map((deg) => (
            <line
              key={deg}
              x1="30" y1="130" x2="15" y2="130"
              stroke="#484f58" strokeWidth="2"
              transform={`rotate(${deg} 130 130)`}
            />
          ))}

          {/* Needle with Glow */}
          <line
            x1="130" y1="130" x2="40" y2="130"
            stroke="#58a6ff"
            strokeWidth="3"
            strokeLinecap="round"
            transform={`rotate(${needle} 130 130)`}
            style={{ transition: 'transform 0.8s cubic-bezier(0.4, 0, 0.2, 1)', filter: 'drop-shadow(0 0 5px #58a6ff)' }}
          />
          <circle cx="130" cy="130" r="6" fill="#f0f6fc" />

          {/* Labels */}
          <text x="10" y="150" fill="#8b949e" fontSize="10" fontFamily="monospace" fontWeight="bold">STABLE</text>
          <text x="5" y="45" fill="#8b949e" fontSize="10" fontFamily="monospace" fontWeight="bold">WARNIING</text>
          <text x="110" y="10" fill="#8b949e" fontSize="10" fontFamily="monospace" fontWeight="bold">UNSTABLE</text>
          <text x="215" y="45" fill="#8b949e" fontSize="10" fontFamily="monospace" fontWeight="bold">HIGH RISK</text>
          <text x="215" y="150" fill="#8b949e" fontSize="10" fontFamily="monospace" fontWeight="bold">Critical</text>
        </svg>

        {/* Center Readout */}
        <div style={{ 
          position: 'absolute', 
          bottom: '5px', 
          left: '50%', 
          transform: 'translateX(-50%)', 
          textAlign: 'center',
          background: 'radial-gradient(circle, rgba(56,139,253,0.1) 0%, transparent 70%)',
          width: '120px',
          padding: '10px'
        }}>
          <div style={{ fontSize: '36px', fontWeight: 800, color: '#f0f6fc', marginBottom: '-5px' }}>
            {isNaN(score) ? 0 : score}
          </div>
          <div style={{ fontSize: '12px', color, letterSpacing: '2px', fontWeight: 'bold', textTransform: 'uppercase' }}>
            {label}
          </div>
          <div style={{ fontSize: '10px', color: '#484f58', marginTop: '5px' }}>
            {patientName.toUpperCase()} • {bed}
          </div>
        </div>
      </div>
    </div>
  )
}
