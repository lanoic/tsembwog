import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression

from ..database import SessionLocal
from ..models import Certificate, DSRDevice, DSREvent, DSREventRegistration, BTMDevice

class RegoPriceModel:
    """Very lightweight price estimator for REGO/GO.
    Features: source (categorical), amount (MWh), certificate age (days).
    Label: synthetic market price in £/MWh. Trains on synthetic/derived data from DB.
    """
    def __init__(self):
        self.enc = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        self.lin = LinearRegression()
        self.is_fit = False

    def _make_df(self):
        db = SessionLocal()
        rows = db.query(Certificate).all()
        db.close()
        if not rows:
            # fabricate some examples if DB empty
            sources = ['Solar', 'Wind', 'Hydro']
            data = []
            rng = np.random.default_rng(42)
            for _ in range(200):
                src = rng.choice(sources)
                amt = float(rng.uniform(1, 500))
                age = float(rng.uniform(0, 365))
                base = {'Solar': 6.5, 'Wind': 5.8, 'Hydro': 7.2}[src]
                price = base + 0.003*amt - 0.002*age + rng.normal(0, 0.5)
                data.append((src, amt, age, price))
            return pd.DataFrame(data, columns=['source','amount','age_days','price'])
        else:
            data = []
            today = datetime.utcnow()
            for r in rows:
                age = (today - r.issue_date).days
                base = 6.0 + (0.4 if 'Solar' in r.source else 0.0) + (0.2 if 'Wind' in r.source else 0.0)
                price = base + 0.003*r.amount_mwh - 0.002*age
                data.append((r.source, float(r.amount_mwh), float(max(age,0)), float(price)))
            return pd.DataFrame(data, columns=['source','amount','age_days','price'])

    def fit(self):
        df = self._make_df()
        X_cat = self.enc.fit_transform(df[['source']])
        X_num = df[['amount','age_days']].to_numpy()
        X = np.hstack([X_cat, X_num])
        y = df['price'].to_numpy()
        self.lin.fit(X, y)
        self.is_fit = True

    def predict(self, source: str, amount_mwh: float, age_days: float) -> float:
        if not self.is_fit:
            self.fit()
        X_cat = self.enc.transform([[source]])
        X_num = np.array([[amount_mwh, age_days]], dtype=float)
        X = np.hstack([X_cat, X_num])
        return float(self.lin.predict(X)[0])


class DSRRecommender:
    """Greedy allocator: choose devices until the target reduction is met."""
    def recommend(self, event_id: int):
        db = SessionLocal()
        ev = db.query(DSREvent).get(event_id)
        if not ev:
            db.close()
            return {"event_id": event_id, "devices": [], "total_kw": 0.0}
        # fetch all active devices; in a real system we'd filter by owner/eligibility, etc.
        devs = db.query(DSRDevice).filter(DSRDevice.is_active==True).all()
        # Sort by max_kw descending
        devs.sort(key=lambda d: d.max_kw, reverse=True)
        goal = float(ev.target_reduction_kw)
        selected = []
        total = 0.0
        for d in devs:
            if total >= goal: break
            put = min(d.max_kw, goal - total)
            selected.append({"device_id": d.id, "name": d.name, "site": d.site, "commit_kw": float(put)})
            total += put
        db.close()
        return {"event_id": ev.id, "target_kw": goal, "total_kw": total, "selection": selected}


class BTMOptimizer:
    """Simple threshold-based charge/discharge schedule.
    Inputs: device_id, price signal (list of £/kWh), initial SOC from DB.
    Policy: charge when price below p_low; discharge when above p_high.
    """
    def optimize(self, device_id: int, prices: list[float], p_low: float = 0.12, p_high: float = 0.25):
        db = SessionLocal()
        dev = db.query(BTMDevice).get(device_id)
        if not dev:
            db.close()
            return {"schedule": [], "final_soc": None}
        soc = float(dev.current_soc)
        cap = float(max(dev.storage_capacity_kwh, 0.1))
        schedule = []
        step_kwh = cap * 0.1  # 10% step per hour (very simplified limits)
        for i, p in enumerate(prices):
            action = "idle"
            if p <= p_low and soc < 0.99:
                # charge
                delta = min(step_kwh, (1.0 - soc) * cap)
                soc = min(1.0, soc + delta / cap)
                action = f"charge {delta:.2f} kWh"
            elif p >= p_high and soc > 0.01:
                # discharge
                delta = min(step_kwh, soc * cap)
                soc = max(0.0, soc - delta / cap)
                action = f"discharge {delta:.2f} kWh"
            schedule.append({"t": i, "price": float(p), "action": action, "soc": float(soc)})
        db.close()
        return {"device_id": device_id, "schedule": schedule, "final_soc": float(soc)}
