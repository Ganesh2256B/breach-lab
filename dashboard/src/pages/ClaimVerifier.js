import React, { useState } from 'react';
import { Upload, FileCheck, AlertCircle, CheckCircle2 } from 'lucide-react';

const ClaimVerifier = () => {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e) => {
    e.preventDefault();
    setLoading(true);

    // Simulate API call to breach-sentinel/verifier.py
    setTimeout(() => {
      setResult({
        claimed_scope: 5000,
        verified_scope: 124,
        fake_record_count: 4876,
        structural_failures: 12,
        identified_sources: ['S3_BUCKET', 'DATABASE'],
        is_authentic: true,
        authenticity_score: 0.0248,
      });
      setLoading(false);
    }, 1500);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <header>
        <h2 className="text-3xl font-bold">Claim Verifier</h2>
        <p className="text-slate-400">Verify the authenticity of leaked data samples</p>
      </header>

      <div className="bg-slate-900 p-8 rounded-2xl border border-slate-800 space-y-6 text-center">
        <div className="mx-auto w-16 h-16 bg-blue-500/10 text-blue-500 rounded-full flex items-center justify-center">
          <Upload size={32} />
        </div>
        <div>
          <h3 className="text-xl font-semibold">Upload Leak Sample</h3>
          <p className="text-slate-400 text-sm">Upload a .json file provided by the threat actor</p>
        </div>
        <form onSubmit={handleUpload} className="flex flex-col items-center gap-4">
          <input
            type="file"
            accept=".json"
            onChange={(e) => setFile(e.target.files[0])}
            className="block w-full text-sm text-slate-500
              file:mr-4 file:py-2 file:px-4
              file:rounded-full file:border-0
              file:text-sm file:font-semibold
              file:bg-blue-600 file:text-white
              hover:file:bg-blue-700 cursor-pointer"
          />
          <button
            disabled={!file || loading}
            className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white px-6 py-2 rounded-lg font-medium transition-all"
          >
            {loading ? "Analyzing..." : "Verify Authenticity"}
          </button>
        </form>
      </div >

      {result && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
          <div className="bg-slate-900 p-6 rounded-2xl border border-slate-800 space-y-4">
            <h3 className="text-lg font-semibold flex items-center gap-2">
              <FileCheck size={20} className="text-blue-500" /> Scope Analysis
            </h3>
            <div className="space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Claimed Records:</span>
                <span className="font-mono">{result.claimed_scope.toLocaleString()}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Verified Records:</span>
                <span className="font-mono text-emerald-400">{result.verified_scope.toLocaleString()}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Fake/Invalid Records:</span>
                <span className="font-mono text-red-400">{result.fake_record_count.toLocaleString()}</span>
              </div>
              <div className="pt-3 border-t border-slate-800 flex justify-between font-bold">
                <span>Authenticity Score:</span>
                <span className={result.authenticity_score < 0.1 ? 'text-red-500' : 'text-emerald-500'}>
                  {(result.authenticity_score * 100).toFixed(2)}%
                </span>
              </div>
            </div>
          </div>

          <div className="bg-slate-900 p-6 rounded-2xl border border-slate-800 space-y-4">
            <h3 className="text-lg font-semibold flex items-center gap-2">
              <AlertCircle size={20} className="text-amber-500" /> Attribution
            </h3>
            <div className="flex flex-wrap gap-2">
              {result.identified_sources.map(source => (
                <span key={source} className="px-3 py-1 bg-amber-500/10 text-amber-500 rounded-full text-xs font-bold border border-amber-500/20">
                  {source}
                </span>
              ))}
            </div>
            <div className="p-4 bg-slate-800/50 rounded-xl text-sm text-slate-400 leading-relaxed">
              {result.is_authentic
                ? "The sample contains verified MeridianBank records. Honey-tokens suggest a leak from both the internal database and a cloud storage export."
                : "No authentic records found. This claim is likely a fabrication."}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ClaimVerifier;
