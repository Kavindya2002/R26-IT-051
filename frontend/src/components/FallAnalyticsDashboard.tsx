import React, { useState, useEffect } from 'react';
import Papa from 'papaparse';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, 
  BarChart, Bar, Cell 
} from 'recharts';
import { Activity, AlertCircle, Users, Zap } from 'lucide-react';

// CSV එකේ තියෙන data structure එක define කිරීම
interface DataRow {
  person_id: string;
  age: number;
  gender: string;
  accel_x: number;
  accel_y: number;
  accel_z: number;
  gyro_x: number;
  gyro_y: number;
  gyro_z: number;
  sma: number;
  magnitude: number;
  activity_label: string;
  stability: string;
  risk_level: 'SAFE' | 'RISKY' | 'HIGH' | 'CRITICAL';
  fall_type: string;
}

const HealthDashboard: React.FC = () => {
  const [data, setData] = useState<DataRow[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    // CSV file එක public folder එකේ තියෙන්න ඕනේ
    Papa.parse<DataRow>("/data.csv", {
      download: true,
      header: true,
      dynamicTyping: true,
      complete: (results) => {
        const validData = results.data.filter(row => row.person_id);
        setData(validData);
        setLoading(false);
      },
      error: (error) => {
        console.error("Error parsing CSV:", error);
        setLoading(false);
      }
    });
  }, []);

  // Risk levels ගණනය කිරීම
  const getRiskCount = (level: string) => data.filter(d => d.risk_level === level).length;

  if (loading) return <div className="p-10 text-center">Data Loading...</div>;

  return (
    <div className="p-6 bg-slate-50 min-h-screen font-sans">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-2xl font-bold mb-6 text-slate-800">Elderly Fall Monitoring System</h1>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <StatCard title="Total Patients" value={data.length} icon={<Users />} color="bg-blue-600" />
          <StatCard title="Critical Cases" value={getRiskCount('CRITICAL')} icon={<Zap />} color="bg-red-600" />
          <StatCard title="High Risk" value={getRiskCount('HIGH')} icon={<AlertCircle />} color="bg-orange-500" />
          <StatCard title="Safe" value={getRiskCount('SAFE')} icon={<Activity />} color="bg-green-500" />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Chart 1: Accelerometer Data */}
          <div className="bg-white p-5 rounded-xl shadow-sm border border-slate-200">
            <h3 className="text-lg font-semibold mb-4 text-slate-700">Movement Patterns (Accelerometer)</h3>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={data.slice(0, 15)}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} />
                  <XAxis dataKey="person_id" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="accel_x" stroke="#3b82f6" dot={false} strokeWidth={2} />
                  <Line type="monotone" dataKey="accel_y" stroke="#10b981" dot={false} strokeWidth={2} />
                  <Line type="monotone" dataKey="accel_z" stroke="#6366f1" dot={false} strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Chart 2: SMA vs Magnitude */}
          <div className="bg-white p-5 rounded-xl shadow-sm border border-slate-200">
            <h3 className="text-lg font-semibold mb-4 text-slate-700">Stability Analysis (SMA)</h3>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={data.slice(0, 10)}>
                  <XAxis dataKey="person_id" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="sma" fill="#8884d8" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="magnitude" fill="#82ca9d" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Card Component
const StatCard = ({ title, value, icon, color }: { title: string, value: number, icon: React.ReactNode, color: string }) => (
  <div className="bg-white p-5 rounded-xl shadow-md flex items-center gap-4">
    <div className={`${color} p-3 rounded-lg text-white`}>{icon}</div>
    <div>
      <p className="text-sm text-gray-500 font-medium">{title}</p>
      <p className="text-2xl font-bold">{value}</p>
    </div>
  </div>
);

export default HealthDashboard;