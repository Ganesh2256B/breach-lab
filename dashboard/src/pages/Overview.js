import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { AlertTriangle, ShieldCheck, Clock, Database, Search, Filter } from 'lucide-react';

// This helper will simulate fetching from the detections.json file
const fetchDetections = async () => {
    try {
        // In a real deploy, this would be an API call to the Sentinel
        // For this demo, we simulate the file reading
        const response = await fetch('/api/detections');
        return await response.json();
    } catch (e) {
        return [];
    }
};

const metricsData = [
  { time: '10:00', attacks: 2, detections: 2 },
  { time: '10:10', attacks: 5, detections: 4 },
  { time: '10:20', attacks: 12, detections: 11 },
  { time: '10:30', attacks: 8, detections: 8 },
  { time: '10:40', attacks: 15, detections: 13 },
  { time: '10:50', attacks: 10, detections: 10 },
];

const StatCard = ({ title, value, icon: Icon, color }) => (
  <div className="glass-panel p-6 rounded-2xl flex items-center gap-4">
    <div className={`p-3 rounded-xl ${color}`}>
      <Icon size={24} />
    </div>
    <div>
      <p className="text-sm text-slate-400 font-medium">{title}</p>
      <p className="text-2xl font-bold">{value}</p>
    </div>
  </div>
);

const Overview = () => {
  return (
    <div className="max-w-7xl mx-auto space-y-8 relative">
      <div className="absolute -top-24 -left-24 w-96 h-96 bg-violet-600/20 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute -bottom-24 -right-24 w-96 h-96 bg-purple-600/10 rounded-full blur-3xl pointer-events-none" />

      <header className="relative z-10">
        <h2 className="text-4xl font-bold text-white mb-2">SOC <span className="text-gradient">Overview</span></h2>
        <p className="text-slate-400">Real-time security posture for MeridianBank</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 relative z-10">
        <StatCard title="Total Attacks" value="142" icon={AlertTriangle} color="bg-red-500/10 text-red-500" />
        <StatCard title="Detections" value="138" icon={ShieldCheck} color="bg-emerald-500/10 text-emerald-500" />
        <StatCard title="Avg. Time to Detect" value="1.2s" icon={Clock} color="bg-violet-500/10 text-violet-500" />
        <StatCard title="Canaries Tripped" value="12" icon={Database} color="bg-purple-500/10 text-purple-500" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 relative z-10">
        <div className="glass-panel p-6 rounded-2xl">
          <h3 className="text-lg font-semibold mb-6 text-white">Attack Volume vs Detections</h3>
          <div className="h-[300px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={metricsData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="time" stroke="#64748b" />
                <YAxis stroke="#64748b" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #9312ff' }}
                  itemStyle={{ color: '#f8fafc' }}
                />
                <Line type="monotone" dataKey="attacks" stroke="#ef4444" strokeWidth={3} dot={{ r: 4 }} />
                <Line type="monotone" dataKey="detections" stroke="#9312ff" strokeWidth={3} dot={{ r: 4 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="glass-panel p-6 rounded-2xl">
          <h3 className="text-lg font-semibold mb-6 text-white">Detection Distribution</h3>
          <div className="h-[300px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={[
                { name: 'IDOR', value: 85 },
                { name: 'S3 Leak', value: 32 },
                { name: 'Vendor', value: 14 },
                { name: 'Creds', value: 7 },
              ]}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="name" stroke="#64748b" />
                <YAxis stroke="#64748b" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #9312ff' }}
                  itemStyle={{ color: '#f8fafc' }}
                />
                <Bar dataKey="value" fill="#9312ff" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Overview;
