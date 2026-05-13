
import React, { useState, useEffect } from 'react';
import { Patient } from '../lib/supabase';

interface Props {
    patients: Patient[];
}

export default function EmergencyAlert({ patients }: Props) {
    const [alertPatient, setAlertPatient] = useState<Patient | null>(null);
    const [isVisible, setIsVisible] = useState(false);



    /*
    useEffect(() => {
      const interval = setInterval(() => {
        if (isVisible) return; 
  
        // High Risk or Critical patients
        const riskyPatients = patients.filter(p => p.status === 'critical' || p.risk_score > 80);
  
        if (riskyPatients.length > 0) {
          const randomPatient = riskyPatients[Math.floor(Math.random() * riskyPatients.length)];
          setAlertPatient(randomPatient);
          setIsVisible(true);
  
          // remove after 15 sec
          setTimeout(() => setIsVisible(false), 15000);
        }
      }, 1000); // sec 1 check
  
      return () => clearInterval(interval);
    }, [patients, isVisible]);
    */

    useEffect(() => {
        const interval = setInterval(() => {
            if (isVisible) return;
            const riskyPatients = patients.filter(p => p.status === 'critical' || p.risk_score > 80);
            if (riskyPatients.length > 0) {
                const randomPatient = riskyPatients[Math.floor(Math.random() * riskyPatients.length)];
                setAlertPatient(randomPatient);
                setIsVisible(true);
            }
        }, 15000);
        return () => clearInterval(interval);
    }, [patients, isVisible]);

    if (!isVisible || !alertPatient) return null;

    if (!isVisible || !alertPatient) return null;

    const getAlertDetails = (score: number) => {
        if (score > 90) return {
            reason: "Critical imbalance & high fall probability detected.",
            action: "Immediate bedside assistance required. Secure the patient."
        };
        return {
            reason: "Sudden deviation in gait symmetry and posture.",
            action: "Check patient stability and verify sensor alignment."
        };
    };

    const details = getAlertDetails(alertPatient.risk_score);


    return (
        <div style={{
            position: 'fixed',
            top: 0,
            left: 0,
            width: '100vw',
            height: '100vh',
            backgroundColor: 'rgba(0, 0, 0, 0.9)', 
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 99999, 
            pointerEvents: 'all'
        }}>

            {/* Alert Box එක */}
            <div style={{
                position: 'relative', 
                width: '90%',
                maxWidth: '600px',
                backgroundColor: '#161b22',
                border: '4px solid #f85149',
                borderRadius: '20px',
                padding: '50px 20px',
                textAlign: 'center',
                boxShadow: '0 0 100px rgba(248, 81, 73, 0.6)',
                animation: 'pulse 1.5s infinite'

            }}>

                <button
                    onClick={() => setIsVisible(false)}
                    style={{
                        zIndex: 1, // box එකට යට නොවීමට
                        position: 'absolute',
                        top: '15px',
                        right: '15px',
                        background: 'transparent',
                        border: 'none',
                        color: '#6e7681',
                        fontSize: '24px',
                        cursor: 'pointer',
                        fontWeight: 'bold'
                    }}
                >✕</button>
                <h1 style={{ color: '#f85149', fontSize: '45px', margin: '0 0 20px 0', fontWeight: '900' }}>
                    ⚠️ EMERGENCY
                </h1>

                <div style={{ margin: '30px 0' }}>
                    <p style={{ color: '#8b949e', fontSize: '18px', textTransform: 'uppercase' }}>High Risk Detected In</p>
                    <h2 style={{ color: '#ffffff', fontSize: '35px', margin: '10px 0' }}>{alertPatient.name}</h2>
                    <p style={{ color: '#f85149', fontSize: '24px', fontWeight: 'bold' }}>BED: {alertPatient.bed}</p>
                </div>

                <div style={{ fontSize: '20px', color: '#c9d1d9', background: 'rgba(248, 81, 73, 0.1)', padding: '15px', borderRadius: '10px' }}>
                    Current Risk Score: <span style={{ color: '#f85149', fontWeight: 'bold' }}>{alertPatient.risk_score}%</span>
                </div>

                <div style={{ textAlign: 'left', background: '#0d1117', padding: '20px', borderRadius: '12px', border: '1px solid #30363d' , marginTop:'10px'}}>
                    <div style={{ marginBottom: '15px' }}>
                        <span style={{ color: '#8b949e', fontSize: '12px', textTransform: 'uppercase', letterSpacing: '1px' }}>Reason for Alert</span>
                        <p style={{ color: '#c9d1d9', fontSize: '16px', margin: '5px 0' }}>{details.reason}</p>
                    </div>
                    
                    <div>
                        <span style={{ color: '#f85149', fontSize: '12px', textTransform: 'uppercase', letterSpacing: '1px', fontWeight: 'bold' }}>Required Action</span>
                        <p style={{ color: '#ffffff', fontSize: '16px', margin: '5px 0', fontWeight: '500' }}>{details.action}</p>
                    </div>
                </div>

                <button 
                    onClick={() => setIsVisible(false)}
                    style={{
                        marginTop: '25px', width: '100%', background: '#f85149', color: 'white',
                        border: 'none', padding: '12px', borderRadius: '8px', 
                        fontWeight: 'bold', fontSize: '16px', cursor: 'pointer'
                    }}
                >
                    ACKNOWLEDGE & CLOSE
                </button>
            </div>



            

            <style>{`
        @keyframes pulse {
          0% { transform: scale(1); }
          50% { transform: scale(1.02); }
          100% { transform: scale(1); }
        }
      `}</style>
        </div>
    );
}