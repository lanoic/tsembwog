import React, { useEffect, useState } from 'react';
import api from '../api';

export default function AdminFlags(){
  const [flags, setFlags] = useState({});
  const [error, setError] = useState(null);

  const load = async ()=>{
    try {
      const { data } = await api.get('/admin/flags');
      setFlags(data);
    } catch(e){
      setError('Admin only or server error.');
    }
  };

  const toggle = async (k)=>{
    const { data } = await api.post('/admin/flags', { key: k, value: !flags[k] });
    setFlags(data);
  }

  useEffect(()=>{ load(); },[]);
  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold mb-4">Feature Flags</h2>
      {error && <div className="text-red-500">{error}</div>}
      <ul className="space-y-2">
        {Object.keys(flags).map(k=> (
          <li key={k} className="flex items-center justify-between border rounded p-2">
            <span>{k}</span>
            <button className="px-3 py-1 border rounded" onClick={()=>toggle(k)}>{flags[k] ? 'ON' : 'OFF'}</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
