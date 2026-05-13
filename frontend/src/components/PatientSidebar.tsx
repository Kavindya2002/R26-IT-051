import React from 'react';

interface PatientSidebarProps {
  patientList: string[];
  activePatientId: string;
  onPatientSelect: (id: string) => void;
}

const PatientSidebar: React.FC<PatientSidebarProps> = ({ patientList, activePatientId, onPatientSelect }) => {
  return (
    <div style={{ 
      width: '280px', 
      background: '#161b22', 
      borderRight: '1px solid #21262d', 
      overflowY: 'auto' 
    }}>
      <div style={{ padding: '20px', fontWeight: 'bold', fontSize: '12px', color: '#8b949e' }}>
        WARD PATIENTS
      </div>
      {patientList.map(id => (
        <div 
          key={id} 
          onClick={() => onPatientSelect(id)}
          style={{ 
            padding: '15px', 
            cursor: 'pointer', 
            background: activePatientId === id ? '#1f242c' : 'transparent', 
            borderLeft: activePatientId === id ? '4px solid #c0392b' : '4px solid transparent',
            transition: '0.2s ease',
            color: activePatientId === id ? '#ffffff' : '#c9d1d9'
          }}
        >
          {id}
        </div>
      ))}
    </div>
  );
};

export default PatientSidebar;


