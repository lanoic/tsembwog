import pulp
from typing import List, Dict
from ..database import SessionLocal
from ..models import DSRDevice, DSREvent, BTMDevice

def lp_allocate_dsr(event_id: int) -> Dict:
    db = SessionLocal()
    ev = db.query(DSREvent).get(event_id)
    if not ev:
        db.close(); return {"event_id": event_id, "selection": [], "total_kw": 0.0}
    devs = db.query(DSRDevice).filter(DSRDevice.is_active==True).all()
    db.close()
    # LP: minimize overcommitment while meeting target
    prob = pulp.LpProblem("DSRAllocation", pulp.LpMinimize)
    x = {d.id: pulp.LpVariable(f"x_{d.id}", lowBound=0, upBound=float(d.max_kw)) for d in devs}
    prob += pulp.lpSum([x[i] for i in x])  # minimize total committed kW
    prob += pulp.lpSum([x[i] for i in x]) >= float(ev.target_reduction_kw)
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    sel = [{"device_id": i, "commit_kw": float(v.value())} for i,v in x.items() if (v.value() or 0) > 1e-6]
    total = float(sum(s["commit_kw"] for s in sel))
    return {"event_id": ev.id, "target_kw": float(ev.target_reduction_kw), "total_kw": total, "selection": sel}

def mpc_schedule(device_id: int, prices: List[float], eta_c: float=0.95, eta_d: float=0.95):
    # Simple linear MPC: choose charge/discharge (kWh) per period to minimize cost
    # s_{t+1} = s_t + eta_c*c_t - d_t/eta_d ; 0 <= s_t <= 1*cap
    # 0 <= c_t, d_t <= step_limit
    db = SessionLocal(); dev = db.query(BTMDevice).get(device_id); db.close()
    if not dev: return {"device_id": device_id, "schedule": [], "final_soc": None}
    H = len(prices); cap = max(float(dev.storage_capacity_kwh), 0.1); s0 = float(dev.current_soc)*cap
    step = 0.1*cap  # 10% per period
    prob = pulp.LpProblem("BTM_MPC", pulp.LpMinimize)
    c = [pulp.LpVariable(f"c_{t}", lowBound=0, upBound=step) for t in range(H)]
    d = [pulp.LpVariable(f"d_{t}", lowBound=0, upBound=step) for t in range(H)]
    s = [pulp.LpVariable(f"s_{t}", lowBound=0, upBound=cap) for t in range(H+1)]
    prob += s[0] == s0
    for t in range(H):
        prob += s[t+1] == s[t] + eta_c*c[t] - d[t]/eta_d
        # Optional: prevent simultaneous c & d (relaxed here)
    # Minimize energy cost: price * (c - d)
    prob += pulp.lpSum([prices[t]*(c[t] - d[t]) for t in range(H)])
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    schedule = []
    for t in range(H):
        schedule.append({"t": t, "price": float(prices[t]), "charge_kwh": float(c[t].value()), "discharge_kwh": float(d[t].value()), "soc": float((s[t+1].value())/cap)})
    return {"device_id": device_id, "schedule": schedule, "final_soc": float((s[-1].value())/cap)}
