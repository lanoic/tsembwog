import React, { useState } from 'react';
import api from '../api';

export default function AdminOps(){
  const [taskId, setTaskId] = useState(null);
  const train = async ()=>{
    const { data } = await api.post('/queue/train-now');
    setTaskId(data.task_id);
  };
  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold mb-2">Admin · Ops</h2>
      <button className="px-3 py-1 border rounded" onClick={train}>Enqueue Model Retrain</button>
      {taskId && <div className="mt-2 text-sm">Task queued: {taskId}</div>}
    </div>
  );
}
