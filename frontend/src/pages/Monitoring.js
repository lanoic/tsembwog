import React, { useEffect, useState } from 'react';

export default function Monitoring(){
  const [text, setText] = useState('');
  useEffect(()=>{
    const url = (process.env.REACT_APP_API_URL || 'http://localhost:8000') + '/metrics';
    fetch(url).then(r=>r.text()).then(setText).catch(()=>setText('Metrics unavailable'));
  },[]);
  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold mb-4">Prometheus Metrics</h2>
      <pre className="text-xs bg-gray-100 dark:bg-gray-800 p-3 rounded overflow-auto">{text}</pre>
    </div>
  );
}
