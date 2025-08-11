import React, { useEffect, useState } from 'react';
import api from '../api';

export default function AdminOrgs(){
  const [orgs, setOrgs] = useState([]);
  const [name, setName] = useState('');

  const load = async ()=>{
    const { data } = await api.get('/admin/orgs');
    setOrgs(data);
  };
  const createOrg = async ()=>{
    if(!name.trim()) return;
    await api.post('/admin/orgs/create', null, { params: { name } });
    setName(''); load();
  };

  useEffect(()=>{ load(); },[]);

  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold mb-4">Admin · Organizations</h2>
      <div className="flex space-x-2 mb-4">
        <input className="border p-1" placeholder="New org name" value={name} onChange={e=>setName(e.target.value)} />
        <button className="px-3 py-1 border rounded" onClick={createOrg}>Create</button>
      </div>
      <ul className="space-y-2">
        {orgs.map(o => (<li key={o.id} className="border rounded p-2">{o.name}</li>))}
      </ul>
    </div>
  );
}
