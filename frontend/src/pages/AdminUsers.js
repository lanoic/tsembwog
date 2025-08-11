import React, { useEffect, useState } from 'react';
import api from '../api';

export default function AdminUsers(){
  const [users, setUsers] = useState([]);
  const [role, setRole] = useState({});

  const load = async () => {
    const { data } = await api.get('/admin/users');
    setUsers(data);
  };

  const saveRole = async (id) => {
    const r = role[id] || 'member';
    await api.post(`/admin/users/${id}/role`, null, { params: { role: r } });
    load();
  };

  useEffect(()=>{ load(); },[]);

  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold mb-4">Admin · Users</h2>
      <table className="w-full text-sm">
        <thead><tr><th>ID</th><th>Email</th><th>Admin</th><th>Role</th><th>Action</th></tr></thead>
        <tbody>
          {users.map(u => (
            <tr key={u.id}>
              <td>{u.id}</td>
              <td>{u.email}</td>
              <td>{u.is_admin ? 'Yes' : 'No'}</td>
              <td>
                <select className="border p-1" value={role[u.id] ?? u.role} onChange={e=>setRole({...role, [u.id]: e.target.value})}>
                  <option>member</option>
                  <option>operator</option>
                  <option>analyst</option>
                  <option>admin</option>
                </select>
              </td>
              <td><button className="px-3 py-1 border rounded" onClick={()=>saveRole(u.id)}>Save</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
