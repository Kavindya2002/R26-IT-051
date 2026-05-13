import React, { useEffect, useRef, useState, useMemo } from 'react';
import { Chart, registerables } from 'chart.js';
import Papa from 'papaparse';
import Patient3DView from './Patient3DView';
import LiveRiskMeter from './LiveRiskMeter';
//import './style.css';

Chart.register(...registerables);

interface FallLog {
  id: string;
  patient_id: string;
  risk_score: number;
  activity: string;
  fall_type: string;
  magnitude: number;
  sma: number;
  created_at: string;
}
interface PatientData {
  person_id: string;
  battery_level: number;
  heart_rate: number;
  signal_strength: number;
  latency: number;
}

interface Props {
  pData: PatientData | null;
}

/*
const REFRESH_RATE = 20;  // 50 kloth 1 sec 10 rows, 20 - 1sec 20 wrows
const SECONDS_PER_ROW = 60;
const STEPS_PER_ROW = (SECONDS_PER_ROW * 1000) / REFRESH_RATE;  
*/
const REFRESH_RATE = 20; 
const SECONDS_PER_ROW = 60;   //4
const STEPS_PER_ROW = (SECONDS_PER_ROW * 1000) / REFRESH_RATE; 

const CHART_LAYOUT = [
  { id: 'intensity_timeline', title: 'MOVEMENT INTENSITY TIMELINE' },
  { id: 'sensor_orientation', title: 'Sensor Orientation (6-Axis)' },
  { id: 'activity_dist', title: 'Activity Distribution' },
  { id: 'risk_gauge', title: 'Stability vs. Risk Gauge' }
];


export default function GaitAnalysisDashboard() {
  const [patientList, setPatientList] = useState<string[]>([]);
  const [groupedData, setGroupedData] = useState<Record<string, any[]>>({});
  const [activePatientId, setActivePatientId] = useState<string>("");
  const [liveStreams, setLiveStreams] = useState<Record<string, any[]>>({});
  const [smoothedScore, setSmoothedScore] = useState(0);
  const [alertData, setAlertData] = useState<any>(null);
  const [logs, setLogs] = useState<FallLog[]>([]);
  const [acknowledgedAlerts, setAcknowledgedAlerts] = useState<string[]>([]);

  const chartRefs = useRef<Record<string, Chart>>({});
  const rowIndicesRef = useRef<Record<string, number>>({});
  const stepIndicesRef = useRef<Record<string, number>>({});
  const lastAlertTimeRef = useRef<Record<string, number>>({});
  const waveOffsetRef = useRef<number>(0);

  const [iotData, setIotData] = useState<Record<string, any>>({});
  const [iotAlert, setIotAlert] = useState<any>(null);


  const [searchTerm, setSearchTerm] = useState('');

  const latestData = liveStreams[activePatientId]?.slice(-1)[0] || {
    activity_label: "Stable",
    accel_x: 0, accel_y: 0, accel_z: 9.8,
    magnitude: 9.8, sma:
      0, stability: "Stable"
  };
  //  Filter states
  const [filters, setFilters] = useState({
    gender: 'All',
    stability: 'All',
    risk_level: 'All',
    fall_type: 'All'
  });





  // data list for filter
  const filteredPatientList = useMemo(() => {
    return patientList.filter(pId => {
      // 1. Search Term check(Patient ID)
      const matchesSearch = pId.toLowerCase().includes(searchTerm.toLowerCase());

      // if searchnot match
      if (!matchesSearch) return false;

      const pDataRows = groupedData[pId];
      if (!pDataRows) return false;

      // check atleast 1 match to filter option
      return pDataRows.some(row => {
        const matchGender = filters.gender === 'All' ||
          String(row.gender).trim().toLowerCase() === filters.gender.toLowerCase();

        const matchStability = filters.stability === 'All' ||
          String(row.stability).trim() === filters.stability;

        const matchRisk = filters.risk_level === 'All' ||
          String(row.risk_level).trim() === filters.risk_level;

        const matchFall = filters.fall_type === 'All' ||
          String(row.fall_type).trim() === filters.fall_type;

        return matchGender && matchStability && matchRisk && matchFall;
      });
    });
  }, [patientList, groupedData, filters, searchTerm]);



  // Filter change function 
  const updateFilter = (key: string, value: string) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  // Stats calculation logic
  const currentPatientData = liveStreams[activePatientId] || [];

  // stats calculation 
  const activityCounts = {
    sitting: currentPatientData.filter(d => String(d.activity_label).trim() === "Sitting").length,
    standing: currentPatientData.filter(d => String(d.activity_label).trim() === "Standing").length,
    walking: currentPatientData.filter(d => String(d.activity_label).trim() === "Walking").length,
  };

  const stats = {
    stabilityRate: 0,
    stableCount: 0,
    unstableCount: 0,
    fallEvents: 0,
    highRiskPercentage: 0,
    highRiskCount: 0,
    avgMagnitude: 0,
    maxMagnitude: 0,
    totalReadings: currentPatientData.length
  };

  const activeIotReadings = iotData[activePatientId] || {
    "Battery Level (%)": 0,
    "Signal Strength RSSI (dBm)": 0,
    "Latency (ms)": 0,
    "Heart Rate (bpm)": 0,
    "Magnetometer Compass (°)": 0
  };

  /*
    const PatientMonitoring: React.FC<Props> = ({ pData }) => {
  
      useEffect(() => {
        if (pData) {
          // 
          if (pData.battery_level < 80) {
            alert(`Alert: Patient ${pData.person_id} Battery Low! (${pData.battery_level}%)`);
          }
  
          // 2.heart beat
          if (pData.heart_rate > 100 || pData.heart_rate < 60) {
            alert(`Emergency: Patient ${pData.person_id} Abnormal Heart Rate: ${pData.heart_rate} bpm`);
          }
  
          // 3. Signal Strength 
          if (pData.signal_strength < -90) {
            alert(`Warning: Patient ${pData.person_id} Signal Weak! (${pData.signal_strength} dBm)`);
          }
        }
      }, [pData]);
  
      return null;
    };*/

  // IoT Data Alerts (Battery & Heart Rate)

  ////dataset read
  useEffect(() => {
    Papa.parse("/fall_detection_dataset.csv", {
      download: true, header: true, dynamicTyping: true, skipEmptyLines: true,
      complete: (results) => {
        const data = results.data as any[];
        const groups: Record<string, any[]> = {};
        const ids: string[] = [];
        data.forEach(row => {
          const pId = row.person_id;
          if (!pId) return;
          if (!groups[pId]) {
            groups[pId] = [];
            ids.push(pId);
            rowIndicesRef.current[pId] = 0;
            stepIndicesRef.current[pId] = 0;
          }
          groups[pId].push(row);
        });
        setGroupedData(groups);
        setPatientList(ids);
        if (ids.length > 0) setActivePatientId(ids[0]);
      }
    });
    Papa.parse("/iot_device_data.csv", {
      download: true,
      header: true,
      dynamicTyping: true,
      complete: (results) => {
        const lookup: Record<string, any> = {};
        results.data.forEach((row: any) => {
          if (row.person_id) lookup[row.person_id] = row;
        });
        setIotData(lookup);
      }
    });
    return () => Object.values(chartRefs.current).forEach(c => c.destroy());
  }, []);


  // Live Streaming Logic
  useEffect(() => {
    if (!activePatientId || !groupedData[activePatientId]) return;
    const interval = setInterval(() => {
      setLiveStreams(prev => {
        const patientData = groupedData[activePatientId];
        const currentRowIdx = rowIndicesRef.current[activePatientId] || 0;
        const currentStepIdx = stepIndicesRef.current[activePatientId] || 0;
        const currentRow = patientData[currentRowIdx];

        if (!currentRow) return prev;

        waveOffsetRef.current += 0.2;
        let amplitude = currentRow.activity_label === 'Walking' ? 2.5 : 0.5;
        const wave = Math.sin(waveOffsetRef.current) * amplitude;

        const interpolated = {
          ...currentRow,
          magnitude: currentRow.magnitude + wave
        };

        const currentRisk = calculateAdvancedRisk(interpolated);

        // 2. Smoothed Score  update 
        setSmoothedScore(prevScore => prevScore + (currentRisk - prevScore) * 0.15);

        const currentStream = prev[activePatientId] || [];
        const updatedStream = [...currentStream, interpolated].slice(-50);

        //const magRisk = Math.abs((interpolated.magnitude || 9.8) - 9.8) * 10;
        //const movementRisk = (interpolated.sma || 0) * 5;
        //const stabilityVal = interpolated.stability === "Stable" ? 0 : 30;
        //const rawTotalScore = Math.min(Math.round(magRisk + movementRisk + stabilityVal), 100);

        //setSmoothedScore(ps => ps + (rawTotalScore - ps) * 0.1);
        //setSmoothedScore(prev => prev + (rawTotalScore - prev) * 0.02);

        let nextStep = currentStepIdx + 1;
        if (nextStep >= STEPS_PER_ROW) {
          nextStep = 0;
          rowIndicesRef.current[activePatientId] = (currentRowIdx + 1) % patientData.length;
        }
        stepIndicesRef.current[activePatientId] = nextStep;
        return { ...prev, [activePatientId]: updatedStream };
      });
    }, REFRESH_RATE);
    return () => clearInterval(interval);
  }, [activePatientId, groupedData]);


  //cards
  if (stats.totalReadings > 0) {
    // 1. Stable Count
    // all csv records get
    const allPatientData = groupedData[activePatientId] || [];
    const totalRows = allPatientData.length;

    if (totalRows > 0) {
      // 1. "Stable" rows count
      const totalStableCount = allPatientData.filter(d =>
        String(d.stability).trim().toLowerCase() === "stable"
      ).length;
      // Stability Rate  (Percentage)
      stats.stabilityRate = Math.round((totalStableCount / totalRows) * 100);
      // stats object 
      stats.stableCount = totalStableCount;
      stats.totalReadings = totalRows; // Dashboard  "out of ..." 
    }
    // 2. dataset -> unstable rows
    stats.unstableCount = (groupedData[activePatientId] || []).filter(d =>
      String(d.stability).trim().toLowerCase() === "unstable"
    ).length;

    // 3. Fall Events (No Fall not)
    // patients all rows
    const allDataForPatient = groupedData[activePatientId] || [];

    if (allDataForPatient.length > 0) {
      stats.fallEvents = allDataForPatient.filter(d => {
        const type = String(d.fall_type || "").trim().toLowerCase();
        // count(Forward/Backward/Lateral Fall) 
        return type !== "" && type !== "no fall";
      }).length;
    }
    // 4. Magnitude Stats (full CSV )
    if (totalRows > 0) {
      // from all data get magnitude data into Array 
      const allMagnitudes = allPatientData.map(d => Number(d.magnitude) || 0);
      // get avg- sum of magnitude value/ rows
      const totalSum = allMagnitudes.reduce((a, b) => a + b, 0);
      const avgVal = totalSum / totalRows;
      // (Max) 
      const maxVal = Math.max(...allMagnitudes);

      // stats object value- 3 decimal
      stats.avgMagnitude = Number(avgVal.toFixed(3));
      stats.maxMagnitude = Number(maxVal.toFixed(3));
    }
  }


  //Risk score calculate
  const calculateAdvancedRisk = (row: any) => {
    let score = 0;

    // 1. G-Force / Impact Analysis (Magnitude)
    //  9.8 - diffeence
    const magDiff = Math.abs((row.magnitude || 9.8) - 9.8);
    const impactScore = Math.min(magDiff * 12, 40); // Max 40%

    // 2. Stability & Fall History (Stability)
    let stabilityScore = 0;
    if (row.stability === "Unstable") {
      stabilityScore = 10;
    }
    // when identify fall
    if (row.fall_type && row.fall_type !== "No Fall") {
      stabilityScore += 10;
    }

    // 3. Movement Intensity (SMA)
    // walking- sma normal, sitdown sma - abnormal
    const smaBase = row.sma || 0;
    let movementScore = 0;
    if (row.activity_label === "Standing" && smaBase > 0.5) {
      movementScore = 30; // standuo and gdk helwenw
    } else {
      movementScore = Math.min(smaBase * 8, 30);
    }

    score = impactScore + stabilityScore + movementScore;
    return Math.min(Math.round(score), 100);
  };


  //Charts
  // Chart Rendering Logic
  useEffect(() => {
    const currentStream = liveStreams[activePatientId];
    if (!currentStream || currentStream.length === 0) return;

    CHART_LAYOUT.forEach(config => {
      const canvas = document.getElementById(config.id) as HTMLCanvasElement;
      if (!canvas) return;
      let chartConfig: any;
      //Intensity Timeline (Line Chart)
      if (config.id === 'intensity_timeline') {
        chartConfig = {
          type: 'line',
          data: {
            labels: currentStream.map((_, i) => i),
            datasets: [{
              label: 'Intensity',
              data: currentStream.map(d => d.magnitude),
              borderColor: '#5dade2',
              borderWidth: 2,
              tension: 0.4, //smooth
              fill: true,
              backgroundColor: 'rgba(93, 173, 226, 0.1)',
              pointRadius: 0,
            }]
          },
          options: {
            responsive: true, maintainAspectRatio: false, animation: { duration: 0 },
            scales: { y: { min: 0, max: 25 }, x: { display: false } },
            plugins: { legend: { display: false } }
          }
        };
      }
      //Intensity Timeline (Line Chart)
      else if (config.id === 'sensor_orientation') {
        const lastData = currentStream[currentStream.length - 1] || {};
        chartConfig = {
          type: 'radar',
          data: {
            labels: ['Acc X', 'Acc Y', 'Acc Z', 'Gyr X', 'Gyr Y', 'Gyr Z'],
            datasets: [{
              data: [lastData.accel_x, lastData.accel_y, lastData.accel_z, lastData.gyro_x, lastData.gyro_y, lastData.gyro_z],
              backgroundColor: 'rgba(130, 80, 223, 0.2)',
              borderColor: '#8250df',
              pointBackgroundColor: '#8250df'
            }]
          },
          options: { scales: { r: { grid: { color: '#333' }, ticks: { display: false } } }, plugins: { legend: { display: false } } }
        };
      }
      //Activity Distribution (Polar Area Chart)
      else if (config.id === 'activity_dist') {
        // get all patient data
        const allPatientData = groupedData[activePatientId] || [];

        const counts: Record<string, number> = { Sitting: 0, Standing: 0, Walking: 0 };

        // count activities
        allPatientData.forEach(d => {
          const label = d.activity_label?.toString().trim();
          if (counts[label] !== undefined) {
            counts[label]++;
          }
        });
        chartConfig = {
          type: 'polarArea', // Doughnut -> Polar Area 
          data: {
            labels: ['Sitting', 'Standing', 'Walking'],
            datasets: [{
              data: [counts.Sitting, counts.Standing, counts.Walking],
              backgroundColor: [
                'rgba(255, 149, 0, 0.6)', // Sitting - Orange
                'rgba(255, 204, 0, 0.6)', // Standing - Yellow
                'rgba(40, 201, 65, 0.6)'   // Walking - Green
              ],
              borderColor: ['#ff9500', '#ffcc00', '#28c941'],
              borderWidth: 1
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              r: {
                grid: { color: '#30363d' },
                angleLines: { color: '#30363d' },
                ticks: { display: false }
              }
            },
            plugins: {
              legend: {
                position: 'bottom',
                labels: { color: '#8b949e', font: { size: 10 } }
              }
            }
          }
        };
      }
      //Risk Gauge (Doughnut Chart)
      else if (config.id === 'risk_gauge') {
        const lastRisk = latestData.risk_level === 'SAFE' ? 20 : 85;
        chartConfig = {
          type: 'doughnut',
          data: {
            datasets: [{
              data: [lastRisk, 100 - lastRisk],
              backgroundColor: [lastRisk > 50 ? '#ff3b30' : '#28c941', '#1c1c1e'],
              circumference: 180, rotation: 270, borderWidth: 0
            }]
          },
          options: { cutout: '80%', plugins: { legend: { display: false } } }
        };
      }
      // Update or Create Chart
      if (chartRefs.current[config.id]) {
        chartRefs.current[config.id].data = chartConfig.data;
        chartRefs.current[config.id].update('none');
      } else {
        chartRefs.current[config.id] = new Chart(canvas, chartConfig);
      }
    });
  }, [activePatientId, liveStreams, latestData]);


  //dashbord create for selected patient
  const handlePatientChange = (id: string) => {
    setActivePatientId(id);
    setLiveStreams({});
    waveOffsetRef.current = 0;
  };

  /*
  const handleAcknowledge = () => {
    if (!alertData) return;
    const newLog: FallLog = {
      id: Math.random().toString(36).substr(2, 9),
      patient_id: alertData.id, risk_score: alertData.score,
      activity: alertData.activity, fall_type: alertData.fallType,
      magnitude: parseFloat(alertData.magnitude), sma: parseFloat(alertData.sma),
      created_at: new Date().toISOString()
    };
    setLogs(prev => [newLog, ...prev].slice(0, 10));
    setAcknowledgedAlerts(prev => [...prev, alertData.id]);
    setAlertData(null);

  };
*/


  //Alerts - device
  useEffect(() => {
    if (activeIotReadings) {
      const battery = activeIotReadings["Battery Level (%)"];
      const heartRate = activeIotReadings["Heart Rate (bpm)"];

      // Battery Alert
      if (battery > 0 && battery < 30) {
        setIotAlert({
          type: 'BATTERY',
          title: 'LOW BATTERY WARNING',
          message: `Device battery is at ${battery}%. Please charge immediately.`,
          value: `${battery}%`,
          color: '#ffa500' // Orange for warning
        });
      }

      // Heart Rate Alert
      if (heartRate > 100 || (heartRate > 0 && heartRate < 60)) {
        setIotAlert({
          type: 'HEART_RATE',
          title: 'ABNORMAL HEART RATE',
          message: heartRate > 100 ? 'Tachycardia detected!' : 'Bradycardia detected!',
          value: `${heartRate} bpm`,
          color: '#ff2e5b' // Red for emergency
        });
      }
    }
  }, [activeIotReadings]);

  //Acknpowledge - Alert
  const handleAcknowledge = () => {
    // 1. Fall Alert eka handle kirima
    if (alertData) {
      const newFallLog: FallLog = {
        id: Math.random().toString(36).substr(2, 9),
        patient_id: alertData.id,
        risk_score: alertData.score,
        activity: alertData.activity,
        fall_type: alertData.fallType,
        magnitude: parseFloat(alertData.magnitude),
        sma: parseFloat(alertData.sma),
        created_at: new Date().toISOString()
      };
      setLogs(prev => [newFallLog, ...prev].slice(0, 10));
      setAcknowledgedAlerts(prev => [...prev, alertData.id]);
      setActivePatientId(alertData.id);
      setAlertData(null);
    }

    // 2. IoT Alert (Battery/Heart Rate) eka handle kireema
    if (iotAlert) {
      const newIotLog: any = {
        id: Date.now().toString(),
        patient_id: activePatientId,
        // Battery nam value eka danna, Heart rate nam number eka witarak ganna
        risk_score: iotAlert.type === 'BATTERY' ? iotAlert.value : iotAlert.value.split(' ')[0],
        fall_type: iotAlert.title, // Meka log eke wisthara widiyata pennanna
        created_at: new Date().toISOString()
      };

      setLogs(prev => [newIotLog, ...prev].slice(0, 10));
      setIotAlert(null);
    }
  };

  //Background Monitor
  useEffect(() => {
    const backgroundMonitor = setInterval(() => {
      patientList.forEach(pId => {
        // skip selectes patient
        if (pId === activePatientId) return;

        const patientData = groupedData[pId];
        const currentIndex = rowIndicesRef.current[pId] || 0;
        const currentRow = patientData[currentIndex];

        if (currentRow) {
          const currentRisk = calculateAdvancedRisk(currentRow);
          // Risk Calculation Logic
          const magRisk = Math.abs((currentRow.magnitude || 9.8) - 9.8) * 10;
          const movementRisk = (currentRow.sma || 0) * 5;
          const stabilityVal = currentRow.stability === "Stable" ? 0 : 30;
          const totalRisk = Math.min(Math.round(magRisk + movementRisk + stabilityVal), 100);

          //device
          const battery = currentRow.battery;
          const heartRate = currentRow.heart_rate;
          const signal = currentRow.signal_strength;
          // 1. Battery Alert (Background)
          if (battery > 0 && battery < 25) {
            setIotAlert({
              type: 'BATTERY',
              title: `CRITICAL BATTERY: ${pId}`,
              message: `Patient ${pId}'s device is at ${battery}%. Please charge.`,
              value: `${battery}%`,
              color: '#ffa500'
            });
          }

          // 2. Heart Rate Alert (Background)
          if (heartRate > 100 || (heartRate > 0 && heartRate < 60)) {
            setIotAlert({
              type: 'HEART_RATE',
              title: `HEART RATE ALERT: ${pId}`,
              message: heartRate > 100 ? `Tachycardia detected for ${pId}!` : `Bradycardia detected for ${pId}!`,
              value: `${heartRate} bpm`,
              color: '#ff2e5b'
            });
          }

          // 3. Signal Strength Alert (Background)
          // -75 dBm වලට වඩා අඩු නම් (උදා: -80, -90) සිග්නල් දුර්වලයි
          if (signal < -75) {
            setIotAlert({
              type: 'SIGNAL',
              title: `WEAK SIGNAL: ${pId}`,
              message: `Device connection for ${pId} is unstable.`,
              value: `${signal} dBm`,
              color: '#ffcc00'
            });
          }

          //fall
          // more than 90% && not  acknowledge yet ->? alert 
          if (totalRisk > 90 && !acknowledgedAlerts.includes(pId)) {
            const now = Date.now();
            const lastAlert = lastAlertTimeRef.current[pId] || 0;

            if (now - lastAlert > 60000) { // trigger after 10 sec
              setAlertData({
                id: pId,
                //score: totalRisk,
                score: currentRisk,
                activity: currentRow.activity_label,
                fallType: totalRisk > 80 ? "CRITICAL FALL" : "STABILITY WARNING",
                magnitude: currentRow.magnitude.toFixed(2),
                sma: currentRow.sma.toFixed(2),
                heartRate: currentRow.heart_rate || "N/A",
                battery: currentRow.battery || "N/A",
                signal: currentRow.signal_strength || "N/A"
              });
              lastAlertTimeRef.current[pId] = now;
            }
          }
        }
      });
    }, 5000); // every 2src bacgorund check 

    return () => clearInterval(backgroundMonitor);
  }, [patientList, groupedData, activePatientId, acknowledgedAlerts]);





  return (
    <div style={{ background: '#0d1117', minHeight: '100vh', display: 'flex', flexDirection: 'column', color: '#c9d1d9', fontFamily: 'sans-serif' }}>
      <div style={{ background: '#161b22', borderBottom: '1px solid #1f6feb', padding: '12px 20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span style={{ fontSize: 16, fontWeight: 700 }}>GAIT MONITOR: {activePatientId}</span>
        <div style={{ padding: '6px 16px', borderRadius: '20px', background: latestData.activity_label === 'Walking' ? '#238636' : '#8e44ad', fontSize: 11 }}>
          STATUS: {latestData.activity_label}
        </div>
      </div>




      <div style={{ display: 'flex', flex: 1, overflow: 'hidden' }}>

        {/* Sidebar 
        <div style={{ width: '250px', background: '#161b22', borderRight: '1px solid #21262d', overflowY: 'auto' }}>
          <div style={{ padding: '20px', fontWeight: 'bold', color: '#8b949e', fontSize: 12 }}>WARD PATIENTS</div>
          {patientList.map(id => (
            <div key={id} onClick={() => handlePatientChange(id)}
              style={{
                padding: '15px', cursor: 'pointer', fontSize: 13,
                background: activePatientId === id ? '#1f242c' : 'transparent',
                borderLeft: activePatientId === id ? '4px solid #3498db' : '4px solid transparent',
                color: acknowledgedAlerts.includes(id) ? '#ff5f57' : '#c9d1d9'
              }}>
              {id} {acknowledgedAlerts.includes(id) && "⚠️"}
            </div>
          ))}
        </div>

        */}

        {/* Sidebar */}
        <div style={{ width: '250px', background: '#161b22', borderRight: '1px solid #21262d', overflowY: 'auto' }}>
          <div style={{ padding: '20px', borderBottom: '1px solid #30363d' }}>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {/* Gender Filter *
              <select
                onChange={(e) => updateFilter('gender', e.target.value)}
                style={{ background: '#0d1117', color: '#c9d1d9', border: '1px solid #30363d', padding: '5px', borderRadius: '10px', fontSize: '12px' }}
              >
                <option value="All">All Genders</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
              </select>

              {/* Stability Filter *
              <select
                onChange={(e) => updateFilter('stability', e.target.value)}
                style={{ background: '#0d1117', color: '#c9d1d9', border: '1px solid #30363d', padding: '5px', borderRadius: '10px', fontSize: '12px' }}
              >
                <option value="All">All Stability</option>
                <option value="Stable">Stable</option>
                <option value="Unstable">Unstable</option>
              </select>

              {/* Risk Level Filter *
              <select
                onChange={(e) => updateFilter('risk_level', e.target.value)}
                style={{ background: '#0d1117', color: '#c9d1d9', border: '1px solid #30363d', padding: '5px', borderRadius: '10px', fontSize: '12px' }}
              >
                <option value="All">All Risk Levels</option>
                <option value="SAFE">Safe</option>
                <option value="RISKY">Risky</option>
              </select>

              {/* Fall Type Filter */}
              <select
                onChange={(e) => updateFilter('fall_type', e.target.value)}
                style={{ background: '#0d1117', color: '#c9d1d9', border: '1px solid #30363d', padding: '5px', borderRadius: '10px', fontSize: '12px' }}
              >
                <option value="All">All Fall Types</option>
                <option value="No Fall">No Fall</option>
                <option value="Forward Fall">Forward Fall</option>
                <option value="Backward Fall">Backward Fall</option>
                <option value="Lateral Fall">Lateral Fall</option>
              </select>
              <div style={{ padding: '10px 20px' }}>
                <input
                  type="text"
                  placeholder="Search Patient ID..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  style={{
                    width: '100%',
                    padding: '8px',
                    background: '#0d1117',
                    color: '#c9d1d9',
                    border: '1px solid #30363d',
                    borderRadius: '10px',
                    fontSize: '13px',
                    outline: 'none'
                  }}
                />
              </div>

             
            </div>
          </div>

          <div style={{ padding: '15px 20px', fontWeight: 'bold', color: '#8b949e', fontSize: 11 }}>
            RESULTS: {filteredPatientList.length}
          </div>

          {/*  patientList  filteredPatientList map  */}
          {filteredPatientList.map(id => (
            <div key={id} onClick={() => handlePatientChange(id)}
              style={{
                padding: '15px', cursor: 'pointer', fontSize: 13,
                background: activePatientId === id ? '#1f242c' : 'transparent',
                borderLeft: activePatientId === id ? '4px solid #3498db' : '4px solid transparent',
                color: acknowledgedAlerts.includes(id) ? '#ff5f57' : '#c9d1d9'
              }}>
              {id} {acknowledgedAlerts.includes(id) && "⚠️"}
            </div>
          ))}
        </div>

        {/* Main Content */}
        <div style={{ flex: 1, padding: '20px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {/* Main Content */}
          <div style={{ flex: 1, padding: '20px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '20px' }}>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '15px' }}>
              {/* Stability Rate Card */}
              <div style={{ background: '#161b22', padding: '15px', borderRadius: '12px', border: '1px solid #30363d' }}>
                <div style={{ fontSize: '11px', color: '#8b949e', fontWeight: 'bold', marginBottom: '8px' }}>STABILITY RATE</div>
                <div style={{ fontSize: '28px', fontWeight: 'bold', color: '#fff' }}>{stats.stabilityRate}%</div>
                <div style={{ fontSize: '11px', color: '#8b949e', marginTop: '4px' }}>{stats.stableCount}/{stats.totalReadings} readings stable</div>
              </div>

              {/* Fall Events Card */}
              <div style={{
                background: '#161b22',
                padding: '15px',
                borderRadius: '12px',
                border: stats.fallEvents > 0 ? '1px solid #ff3b30' : '1px solid #30363d', // fall- red border
                boxShadow: stats.fallEvents > 0 ? '0 0 10px rgba(255, 59, 48, 0.2)' : 'none'
              }}>
                <div style={{ fontSize: '11px', color: '#8b949e', fontWeight: 'bold', marginBottom: '8px' }}>
                  FALL EVENTS (LAST 50)
                </div>
                <div style={{
                  fontSize: '28px',
                  fontWeight: 'bold',
                  color: stats.fallEvents > 0 ? '#ff3b30' : '#fff' // fall- red no
                }}>
                  {stats.fallEvents}
                </div>
                <div style={{ fontSize: '11px', color: '#8b949e', marginTop: '4px' }}>
                  Detected in current window
                </div>
              </div>

              {/* High/Critical Risk Card */}
              {/* Unstable Sessions Card  */}
              <div style={{ background: '#161b22', padding: '15px', borderRadius: '12px', border: '1px solid #30363d', boxShadow: stats.unstableCount > 0 ? 'inset 0 0 10px rgba(255, 149, 0, 0.1)' : 'none' }}>
                <div style={{ fontSize: '11px', color: '#8b949e', fontWeight: 'bold', marginBottom: '8px' }}>UNSTABLE SESSIONS</div>
                <div style={{ fontSize: '28px', fontWeight: 'bold', color: stats.unstableCount > 0 ? '#ff9500' : '#fff' }}>{stats.unstableCount}</div>
                <div style={{ fontSize: '11px', color: '#8b949e', marginTop: '4px' }}>Unstable gait detected</div>
              </div>
              {/*}
              <div style={{ background: '#161b22', padding: '15px', borderRadius: '12px', border: '1px solid #30363d' }}>
                <div style={{ fontSize: '11px', color: '#8b949e', fontWeight: 'bold', marginBottom: '8px' }}>HIGH/CRITICAL RISK</div>
                <div style={{ fontSize: '28px', fontWeight: 'bold', color: '#fff' }}>{stats.highRiskPercentage}%</div>
                <div style={{ fontSize: '11px', color: '#8b949e', marginTop: '4px' }}>{stats.highRiskCount} readings</div>
              </div>
*/}
              {/* Avg Magnitude Card */}
              <div style={{ background: '#161b22', padding: '15px', borderRadius: '12px', border: '1px solid #30363d' }}>
                <div style={{ fontSize: '11px', color: '#8b949e', fontWeight: 'bold', marginBottom: '8px' }}>AVG MAGNITUDE</div>
                <div style={{ fontSize: '28px', fontWeight: 'bold', color: '#fff' }}>{Number(stats.avgMagnitude).toFixed(3)}</div>
                <div style={{ fontSize: '11px', color: '#8b949e', marginTop: '4px' }}>Max: {Number(stats.maxMagnitude).toFixed(3)}</div>
              </div>


              {/* Patient ID */}
              <div style={{ background: '#2c2c2e', padding: '15px', borderRadius: '10px' }}>
                <div style={{ fontSize: '11px', color: '#8b949e' }}>Patient ID</div>
                <div style={{ fontSize: '18px', fontWeight: 'bold' }}>{activePatientId}</div>
              </div>

              {/* Battery Level */}
              <div style={{ background: '#2c2c2e', padding: '15px', borderRadius: '10px' }}>
                <div style={{ fontSize: '11px', color: '#8b949e' }}>Battery Level</div>
                <div style={{ fontSize: '18px', fontWeight: 'bold' }}>{activeIotReadings["Battery Level (%)"]}%</div>
              </div>

              {/* Signal Strength */}
              <div style={{ background: '#2c2c2e', padding: '15px', borderRadius: '10px' }}>
                <div style={{ fontSize: '11px', color: '#8b949e' }}>Signal Strength</div>
                <div style={{ fontSize: '18px', fontWeight: 'bold' }}>{activeIotReadings["Signal Strength RSSI (dBm)"]} dBm</div>
                <div style={{ fontSize: '11px', color: '#8b949e' }}>-30 dBm to -50 dBm</div>
              </div>

              {/* Heart Rate */}
              <div style={{ background: '#2c2c2e', padding: '15px', borderRadius: '10px' }}>
                <div style={{ fontSize: '11px', color: '#8b949e' }}>Heart Rate</div>
                <div style={{ fontSize: '18px', fontWeight: 'bold', color: '#ff3b30' }}>{activeIotReadings["Heart Rate (bpm)"]} bpm</div>
                <div style={{ fontSize: '11px', color: '#8b949e' }}>60 – 100 bpm</div>
              </div>
            </div>

            <div style={{ display: 'flex', gap: '20px' }}>
              <div style={{ flex: 1, background: '#161b22', padding: '20px', borderRadius: '12px' }}>
                <LiveRiskMeter score={Math.round(smoothedScore)} patientName={activePatientId} bed={activePatientId} />
              </div>
              <div style={{ flex: 2, background: '#161b22', padding: '20px', borderRadius: '12px' }}>
                <Patient3DView activity={latestData.activity_label} accel={{ x: latestData.accel_x, y: latestData.accel_y, z: latestData.accel_z }} />
              </div>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
              {CHART_LAYOUT.map(config => (
                <div key={config.id} style={{ background: '#161b22', padding: '20px', borderRadius: '12px', height: '260px' }}>
                  <h4 style={{ color: '#8b949e', fontSize: 12, marginBottom: 10 }}>{config.title}</h4>
                  <canvas id={config.id} />
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Alert Log Sidebar *
        <div style={{ background: '#0d1117', padding: '15px', width: '300px', borderLeft: '1px solid #21262d', overflowY: 'auto' }}>
          <h3 style={{ fontSize: '12px', color: '#8b949e', marginBottom: '20px' }}>SESSION ALERT LOG</h3>
          {logs.map((log) => (
            <div key={log.id} style={{ background: 'rgba(255, 46, 91, 0.05)', border: '1px solid rgba(255, 46, 91, 0.2)', borderRadius: '8px', padding: '12px', marginBottom: '10px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <div style={{ width: 8, height: 8, borderRadius: '50%', background: '#ff2e5b' }}></div>
                <span style={{ color: '#ff2e5b', fontWeight: 'bold', fontSize: '11px' }}>{log.patient_id} - {log.risk_score}%</span>
              </div>
              <p style={{ margin: '5px 0', fontSize: '10px', color: '#c9d1d9' }}>{log.fall_type}</p>
              <span style={{ fontSize: '10px', color: '#8b949e' }}>{new Date(log.created_at).toLocaleTimeString()}</span>
            </div>
          ))}
        </div>

        */}

        {/* Alert Log Sidebar */}
        <div style={{ background: '#0d1117', padding: '15px', width: '300px', borderLeft: '1px solid #21262d', overflowY: 'auto' }}>
          <h3 style={{ fontSize: '12px', color: '#8b949e', marginBottom: '20px' }}>SESSION ALERT LOG</h3>

          {logs.map((log) => {
            // Alert type basec color decide
            // IoT Alert (Title - WARNING or ABNORMAL ) - blue
            const isIotAlert = log.fall_type?.includes("WARNING") || log.fall_type?.includes("ABNORMAL");
            const themeColor = isIotAlert ? '#2e99ff' : '#ff2e5b';
            const bgColor = isIotAlert ? 'rgba(46, 153, 255, 0.05)' : 'rgba(255, 46, 91, 0.05)';
            const borderColor = isIotAlert ? 'rgba(46, 153, 255, 0.2)' : 'rgba(255, 46, 91, 0.2)';

            return (
              <div key={log.id} style={{
                background: bgColor,
                border: `1px solid ${borderColor}`,
                borderRadius: '8px', padding: '12px', marginBottom: '10px'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <div style={{ width: 8, height: 8, borderRadius: '50%', background: themeColor }}></div>
                  <span style={{ color: themeColor, fontWeight: 'bold', fontSize: '11px' }}>
                    {log.patient_id} - {log.risk_score}{isIotAlert ? '' : '%'}
                  </span>
                </div>
                <p style={{ margin: '5px 0', fontSize: '10px', color: '#c9d1d9' }}>{log.fall_type}</p>
                <span style={{ fontSize: '10px', color: '#8b949e' }}>{new Date(log.created_at).toLocaleTimeString()}</span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Alert Overlay */}
      {alertData && (
        <div style={{
          position: 'fixed', top: 0, left: 0, width: '100%', height: '100%',
          background: 'rgba(0,0,0,0.85)', display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 9999
        }}>
          <div style={{
            width: '450px', background: '#0d1117', border: '2px solid #ff2e5b',
            borderRadius: '15px', padding: '25px', boxShadow: '0 0 30px rgba(255, 46, 91, 0.4)', textAlign: 'left'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '15px', marginBottom: '20px' }}>
              <div style={{ color: '#ff2e5b', fontSize: '24px' }}>⚠️</div>
              <h2 style={{ color: '#ff2e5b', margin: 0, fontSize: '18px', fontWeight: 'bold' }}>CRITICAL FALL RISK</h2>
            </div>

            <div style={{ background: 'rgba(255,255,255,0.03)', padding: '20px', borderRadius: '10px', fontSize: '14px', border: '1px solid #21262d' }}>
              <div style={{ display: 'grid', gridTemplateColumns: '120px 1fr', gap: '10px' }}>
                <span style={{ color: '#8b949e' }}>Patient</span> <span style={{ fontWeight: 'bold' }}>{alertData.id}</span>
                <span style={{ color: '#8b949e' }}>Risk Score</span> <span style={{ color: '#ff2e5b', fontWeight: 'bold' }}>{alertData.score}% (CRITICAL)</span>
                <span style={{ color: '#8b949e' }}>Activity</span> <span>{alertData.activity}</span>
                <span style={{ color: '#8b949e' }}>Fall Type</span> <span>{alertData.fallType}</span>
                <span style={{ color: '#8b949e' }}>Magnitude</span> <span>{alertData.magnitude} m/s²</span>
                <span style={{ color: '#8b949e' }}>SMA (Movement)</span> <span>{alertData.sma}</span>

                {/*  <span style={{ color: '#8b949e' }}>Heart Rate</span>
                <span style={{ color: parseInt(alertData.heartRate) > 100 ? '#ff2e5b' : '#fff' }}>
                  {alertData.heartRate} bpm
                </span>

                <span style={{ color: '#8b949e' }}>Movement (SMA)</span> <span>{alertData.sma}</span>

                <span style={{ color: '#8b949e' }}>Stability</span>
                <span style={{ color: alertData.score > 50 ? '#ff2e5b' : '#fff' }}>{alertData.fallType}</span>

                <span style={{ color: '#8b949e' }}>Battery Level</span>
                <span style={{ color: parseInt(alertData.battery) < 20 ? '#ff2e5b' : '#fff' }}>
                  {alertData.battery}%
                </span>

                <span style={{ color: '#8b949e' }}>Signal</span> <span>{alertData.signal} dBm</span>

                {/*(Reason) *
                <span style={{ color: '#8b949e' }}>Reason</span>
                <span style={{ color: '#f85149', fontSize: '12px' }}>
                  {alertData.score > 90 ? "High impact & instability detected" : "Slight movement anomaly"}
                </span> */}

              </div>
            </div>

            <div style={{ display: 'flex', gap: '12px', marginTop: '25px' }}>
              <button onClick={handleAcknowledge} style={{
                flex: 1, padding: '12px', background: '#ff2e5b', color: 'white',
                border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold'
              }}>✓ ACKNOWLEDGE</button>
              <button onClick={() => setAlertData(null)} style={{
                flex: 1, padding: '12px', background: 'transparent', color: '#8b949e',
                border: '1px solid #30363d', borderRadius: '8px', cursor: 'pointer'
              }}>DISMISS</button>
            </div>
          </div>
        </div>
      )}


      {iotAlert && (
        <div style={{
          position: 'fixed', top: 0, left: 0, width: '100%', height: '100%',
          background: 'rgba(0,0,0,0.85)', display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 10000
        }}>
          <div style={{
            width: '400px', background: '#0d1117', border: `2px solid ${iotAlert.color}`,
            borderRadius: '15px', padding: '25px', boxShadow: `0 0 30px ${iotAlert.color}66`, textAlign: 'left'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '15px', marginBottom: '20px' }}>
              <div style={{ fontSize: '24px' }}>{iotAlert.type === 'BATTERY' ? '🔋' : '🚨'}</div>
              <h2 style={{ color: iotAlert.color, margin: 0, fontSize: '18px', fontWeight: 'bold' }}>{iotAlert.title}</h2>
            </div>

            <div style={{ background: 'rgba(255,255,255,0.03)', padding: '20px', borderRadius: '10px', border: '1px solid #21262d' }}>
              <p style={{ color: '#8b949e', margin: '0 0 10px 0', fontSize: '14px' }}>Patient ID: <b>{iotAlert.patientId || activePatientId}</b></p>
              <p style={{ color: 'white', fontSize: '16px', margin: '0 0 10px 0' }}>{iotAlert.message}</p>
              <div style={{ fontSize: '22px', fontWeight: 'bold', color: iotAlert.color }}>{iotAlert.value}</div>
            </div>

            <div style={{ display: 'flex', gap: '12px', marginTop: '25px' }}>
              {/* <button 
          onClick={() => setIotAlert(null)} 
          style={{
            flex: 1, padding: '12px', background: iotAlert.color, color: 'white',
            border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold'
          }}>
          DISMISS
        </button> */}
            </div>
            <div style={{ display: 'flex', gap: '12px', marginTop: '25px' }}>
              <button onClick={handleAcknowledge} style={{
                flex: 1, padding: '12px', background: '#ff2e5b', color: 'white',
                border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold'
              }}>✓ ACKNOWLEDGE</button>
              <button
                onClick={() => setIotAlert(null)}
                style={{
                  flex: 1, padding: '12px', background: 'transparent', color: '#8b949e',
                  border: '1px solid #30363d', borderRadius: '8px', cursor: 'pointer'
                }}>
                DISMISS (Temporary)
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}