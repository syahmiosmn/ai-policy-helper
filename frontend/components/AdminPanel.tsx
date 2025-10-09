'use client';
import React from 'react';
import { apiIngest, apiMetrics, apiHealth } from '@/lib/api';

export default function AdminPanel() {
  const [metrics, setMetrics] = React.useState<any>(null);
  const [health, setHealth] = React.useState<any>(null);
  const [busy, setBusy] = React.useState(false);

  const refresh = async () => {
    const m = await apiMetrics();
    setMetrics(m);
  };

  const ingest = async () => {
    setBusy(true);
    try {
      await apiIngest();
      await refresh();
    } finally {
      setBusy(false);
    }
  };

  const checkHealth = async () => {
    try {
      const h = await apiHealth();
      setHealth(h);
    } catch {
      setHealth('not ok');
    }
  };

  React.useEffect(() => { refresh(); }, []);

  return (
    <div className="card">
      <h2>Admin</h2>
      <div style={{display:'flex', gap:8, marginBottom:8}}>
        <button onClick={ingest} disabled={busy} style={{padding:'8px 12px', borderRadius:8, border:'1px solid #111', background:'#fff'}}>
          {busy ? 'Indexing...' : 'Ingest sample docs'}
        </button>
        <button onClick={refresh} style={{padding:'8px 12px', borderRadius:8, border:'1px solid #111', background:'#fff'}}>Refresh metrics</button>
        <button onClick={checkHealth} style={{ padding: '8px 12px', borderRadius: 8, border: '1px solid #111', background: '#fff' }}>Check Health</button>
      </div>
      {health && (
        <div style={{ marginBottom: 8, fontWeight: 'bold' }}>
          Health: {typeof health === 'string' ? health : JSON.stringify(health, null, 2)}
        </div>
      )}
      {metrics && (
        <div className="code">
          <pre>{JSON.stringify(metrics, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
