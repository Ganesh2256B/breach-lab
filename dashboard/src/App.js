import React from 'react';
import { LayoutDashboard, ShieldAlert, FileSearch, FileText, Activity, Terminal } from 'lucide-react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Overview from './pages/Overview';
import Detections from './pages/Detections';
import ClaimVerifier from './pages/ClaimVerifier';
import Reports from './pages/Reports';

const SidebarItem = ({ to, icon: Icon, label }) => (
  <Link to={to} className="flex items-center gap-3 px-4 py-3 text-green-500 hover:text-white hover:bg-green-900/30 rounded-lg transition-colors font-mono text-sm">
    <Icon size={20} />
    <span className="font-medium uppercase tracking-wider">{label}</span>
  </Link>
);

const App = () => {
  return (
    <BrowserRouter>
      <div className="flex h-screen bg-black text-green-500 font-mono">
        {/* Sidebar */}
        <aside className="w-64 border-r border-green-900/50 flex flex-col p-4 gap-8 bg-black">
          <div className="flex items-center gap-2 px-2">
            <div className="bg-green-600 p-1.5 rounded-sm">
              <Terminal size={24} className="text-black" />
            </div>
            <h1 className="text-xl font-bold tracking-tighter neon-text" style={{ fontFamily: 'Outfit, sans-serif' }}>
              NEURAL_VOID
            </h1>
          </div>

          <nav className="flex flex-col gap-2">
            <SidebarItem to="/" icon={LayoutDashboard} label="Core_Overview" />
            <SidebarItem to="/detections" icon={Activity} label="Threat_Stream" />
            <SidebarItem to="/verify" icon={FileSearch} label="Packet_Verify" />
            <SidebarItem to="/reports" icon={FileText} label="Archive_Logs" />
          </nav>

          <div className="mt-auto p-4 bg-green-900/10 rounded-sm border border-green-900/30">
            <p className="text-xs text-green-700 uppercase font-bold mb-2">System Node</p>
            <div className="flex items-center gap-2 text-sm text-green-400 font-mono">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
              NODE_ACTIVE_01
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
