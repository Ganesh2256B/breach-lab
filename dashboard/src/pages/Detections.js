import React, { useState } from 'react';
import { AlertCircle, Search, Filter } from 'lucide-react';

const Detections = () => {
  const [alerts] = useState([
    { id: 'DET-101', rule: 'RATE_LIMIT_EXCEEDED', summary: 'Potential IDOR scraping detected: 45 requests in 10s', ip: '192.168.1.45', time: '2024-10-25T14:20:01Z', severity: 'MEDIUM' },
    { id: 'DET-102', rule: 'SENSITIVE_PATH_ACCESS', summary: 'Access to protected path: /storage/exports/customer_data_full.json', ip: '45.12.144.10', time: '2024-10-25T14:21:15Z', severity: 'HIGH' },
    { id: 'DET-103', rule: 'SENSITIVE_PATH_ACCESS', summary: 'Access to protected path: /api/internal/sync-job', ip: '10.0.0.5', time: '2024-10-25T14:22:10Z', severity: 'HIGH' },
  ]);

  return (
    <div className="max-w-7xl mx-auto space-y-8 relative">
      <header className="flex justify-between items-center">
        <div>
          <h2 className="text-4xl font-bold text-white mb-2">Live <span className="text-gradient">Detections</span></h2>
          <p className="text-slate-400">Real-time stream of security alerts from Breach Sentinel</p>
        </div>
        <div className="flex gap-3">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" size={18} />
            <input
              type="text"
              placeholder="Filter alerts..."
              className="bg-slate-900 border border-slate-800 rounded-lg pl-10 pr-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500 text-white"
            />
          </div>
          <button className="bg-slate-900 border border-slate-800 p-2 rounded-lg hover:bg-slate-800 text-white">
            <Filter size={18} />
          </button>
        </div>
      </header>

      <div className="glass-panel rounded-2xl overflow-hidden">
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-800/50 text-slate-400 uppercase text-xs font-bold">
            <tr className="border-b border-slate-800">
              <th className="px-6 py-4">Detection ID</th>
              <th className="px-6 py-4">Rule</th>
              <th className="px-6 py-4">Summary</th>
              <th className="px-6 py-4">Source IP</th>
              <th className="px-6 py-4">Severity</th>
              <th className="px-6 py-4">Timestamp</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800">
            {alerts.map((alert) => (
              <tr key={alert.id} className="hover:bg-violet-500/5 transition-colors">
                <td className="px-6 py-4 font-mono text-slate-400">{alert.id}</td>
                <td className="px-6 py-4">
                  <span className="px-2 py-1 bg-violet-900/30 text-violet-400 rounded text-xs font-medium border border-violet-500/20">{alert.rule}</span>
                </td>
                <td className="px-6 py-4 text-slate-300">{alert.summary}</td>
                <td className="px-6 py-4 font-mono text-slate-400">{alert.ip}</td>
                <td className="px-6 py-4">
                  <span className={`px-2 py-1 rounded-full text-[10px] font-bold uppercase ${
                    alert.severity === 'HIGH' ? 'bg-red-500/10 text-red-500' : 'bg-amber-500/10 text-amber-500'
                  }`}>
                    {alert.severity}
                  </span>
                </td>
                <td className="px-6 py-4 text-slate-500">{alert.time}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Detections;
