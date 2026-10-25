import React from 'react';
import { LayoutDashboard, ShieldAlert, FileSearch, FileText, Activity } from 'lucide-react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Overview from './pages/Overview';
import Detections from './pages/Detections';
import ClaimVerifier from './pages/ClaimVerifier';
import Reports from './pages/Reports';

const SidebarItem = ({ to, icon: Icon, label }) => (
  <Link to={to} className="flex items-center gap-3 px-4 py-3 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition-colors">
    <Icon size={20} />
    <span className="font-medium">{label}</span>
  </Link>
);

const App = () => {
  return (
    <BrowserRouter>
      <div className="flex h-screen bg-slate-950 text-slate-100">
        {/* Sidebar */}
        <aside className="w-64 border-r border-slate-800 flex flex-col p-4 gap-8">
          <div className="flex items-center gap-2 px-2">
            <div className="bg-blue-600 p-1.5 rounded-lg">
              <ShieldAlert size={24} className="text-white" />
            </div>
            <h1 className="text-xl font-bold tracking-tight">BreachSentinel</h1>
          </div>

          <nav className="flex flex-col gap-2">
            <SidebarItem to="/" icon={LayoutDashboard} label="SOC Overview" />
            <SidebarItem to="/detections" icon={Activity} label="Live Detections" />
            <SidebarItem to="/verify" icon={FileSearch} label="Claim Verifier" />
            <SidebarItem to="/reports" icon={FileText} label="Incident Reports" />
          </nav>

          <div className="mt-auto p-4 bg-slate-900 rounded-xl border border-slate-800">
            <p className="text-xs text-slate-500 uppercase font-bold mb-2">System Status</p>
            <div className="flex items-center gap-2 text-sm text-emerald-400">
              <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />
              Monitoring Active
            </div>
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 overflow-auto p-8">
          <Routes>
            <Route path="/" element={<Overview />} />
            <Route path="/detections" element={<Detections />} />
            <Route path="/verify" element={<ClaimVerifier />} />
            <Route path="/reports" element={<Reports />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
};

export default App;
