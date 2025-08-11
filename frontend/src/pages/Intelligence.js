import React, { useState } from 'react';
import api from '../api';

export default function Intelligence(){
  // REGO price
  const [src,setSrc]=useState('Solar');
  const [amt,setAmt]=useState(100);
  const [age,setAge]=useState(30);
  const [price,setPrice]=useState(null);

  const predict=async()=>{
    const { data } = await api.post('/ai/rego/price_predict', { source: src, amount_mwh: Number(amt), age_days: Number(age) });
    setPrice(data.price_per_mwh);
  }

  // DSR recommend
  const [eventId,setEventId]=useState('1');
  const [rec,setRec]=useState(null);
  const recommend=async()=>{
    const { data } = await api.get('/ai/dsr/recommend', { params: { event_id: Number(eventId) } });
    setRec(data);
  }

  // BTM optimize
  const [deviceId,setDeviceId]=useState('1');
  const [prices,setPrices]=useState('0.18,0.20,0.10,0.08,0.30,0.26');
  const [plan,setPlan]=useState(null);
  const optimize=async()=>{
    const arr = prices.split(',').map(x=>Number(x.trim())).filter(x=>!isNaN(x));
    const { data } = await api.post('/ai/btm/optimize', { device_id: Number(deviceId), prices: arr });
    setPlan(data);
  }

  return (
    <div className="p-6 space-y-8">
      <section className="border rounded p-4">
        <h3 className="font-semibold">REGO/GO Price Estimation (£/MWh)</h3>
        <div className="space-x-2 mt-2">
          <select value={src} onChange={e=>setSrc(e.target.value)} className="border p-1">
            <option>Solar</option><option>Wind</option><option>Hydro</option>
          </select>
          <input className="border p-1 w-24" value={amt} onChange={e=>setAmt(e.target.value)} />
          <input className="border p-1 w-24" value={age} onChange={e=>setAge(e.target.value)} />
          <button className="px-3 py-1 border rounded" onClick={predict}>Predict</button>
        </div>
        {price!==null && <div className="mt-2 text-sm">Estimated price: <b>£{price.toFixed(3)}</b> / MWh</div>}
      </section>

      <section className="border rounded p-4">
        <h3 className="font-semibold">DSR Event Recommendation</h3>
        <div className="space-x-2 mt-2">
          <input className="border p-1 w-24" value={eventId} onChange={e=>setEventId(e.target.value)} />
          <button className="px-3 py-1 border rounded" onClick={recommend}>Recommend</button>
        </div>
        {rec && <pre className="text-xs mt-2 bg-gray-100 dark:bg-gray-800 p-2 rounded">{JSON.stringify(rec, null, 2)}</pre>}
      </section>

      <section className="border rounded p-4">
        <h3 className="font-semibold">BTM Charge/Discharge Optimization</h3>
        <div className="space-x-2 mt-2">
          <input className="border p-1 w-24" value={deviceId} onChange={e=>setDeviceId(e.target.value)} />
          <input className="border p-1 w-96" value={prices} onChange={e=>setPrices(e.target.value)} />
          <button className="px-3 py-1 border rounded" onClick={optimize}>Optimize</button>
        </div>
        {plan && <pre className="text-xs mt-2 bg-gray-100 dark:bg-gray-800 p-2 rounded">{JSON.stringify(plan, null, 2)}</pre>}
      </section>
    </div>
  );
}
