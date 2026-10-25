import React from 'react';
import { FileText, Download, ExternalLink } from 'lucide-react';

const Reports = () => {
  const reports = [
    { id: 'IR-001', title: 'Incident Timeline - Breach-LAB-001', date: '2024-10-25', type: 'Timeline' },
    { id: 'IR-002', title: 'Full Breach Report - Executive Summary', date: '2024-10-25', type: 'Executive' },
    { id: 'IR-003', title: 'Customer Notification Drafts', date: '2024-10-25', type: 'Communication' },
  ];

  return (
    <div className="max-w-7xl mx-auto space-y-8">
      <header>
        <h2 className="text-3xl font-bold">Incident Reports</h2>
        <p className="text-slate-400">Download and export formal IR artifacts</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {reports.map(report => (
          <div key={report.id} className="bg-slate-900 p-6 rounded-2xl border border-slate-800 hover:border-blue-500 transition-colors group">
            <div className="flex justify-between items-start mb-4">
              <div className="p-2 bg-blue-500/10 text-blue-500 rounded-lg">
                <FileText size={24} />
              </div>
              <span className="text-[10px] font-bold uppercase px-2 py-1 bg-slate-800 text-slate-400 rounded">
                {report.type}
              </span>
            </div>
            <h3 className="font-semibold text-lg mb-1">{report.title}</h3>
            <p className="text-slate-500 text-sm mb-6">Generated on {report.date}</p>
            <div className="flex gap-2">
              <button className="flex-1 flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg text-sm font-medium transition-colors">
                <Download size={16} /> Download
              </button>
              <button className="p-2 bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors text-slate-400">
                <ExternalLink size={16} />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Reports;
