import os, joblib, numpy as np, pandas as pd
from datetime import datetime
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingRegressor

from ..database import SessionLocal
from ..models import Certificate
from ..storage import save_bytes, load_bytes
import io


MODEL_DIR = os.environ.get("MODEL_DIR", "/app/models")
os.makedirs(MODEL_DIR, exist_ok=True)
MODEL_PATH = os.path.join(MODEL_DIR, "rego_price_gb.joblib")

def _derive_training_df():
    db = SessionLocal()
    rows = db.query(Certificate).all()
    db.close()
    data = []
    if not rows:
        rng = np.random.default_rng(7)
        sources = ["Solar","Wind","Hydro","Biomass"]
        for _ in range(500):
            src = rng.choice(sources)
            amt = float(rng.uniform(1, 1000))
            age = float(rng.uniform(0, 365*2))
            base = {"Solar":7.0,"Wind":6.0,"Hydro":7.5,"Biomass":6.8}[src]
            price = base + 0.004*amt - 0.0015*age + rng.normal(0,0.6)
            data.append((src, amt, age, price))
    else:
        today = datetime.utcnow()
        for r in rows:
            age = max((today - r.issue_date).days, 0)
            # heuristic baseline
            base = 6.5 + (0.7 if "Solar" in r.source else 0.0) + (0.3 if "Wind" in r.source else 0.0)
            price = base + 0.004*r.amount_mwh - 0.0015*age
            data.append((r.source, float(r.amount_mwh), float(age), float(price)))
    return pd.DataFrame(data, columns=["source","amount","age_days","price"])

def train_and_save():
    df = _derive_training_df()
    X = df[["source","amount","age_days"]]
    y = df["price"]
    cat = ["source"]; num = ["amount","age_days"]
    pre = ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore"), cat)], remainder="passthrough")
    gb = GradientBoostingRegressor(random_state=42)
    pipe = Pipeline([("pre", pre), ("gb", gb)])
    pipe.fit(X, y)
    buf = io.BytesIO(); joblib.dump(pipe, buf); save_bytes('rego_price_gb.joblib', buf.getvalue()); return 's3://'+os.environ.get('S3_BUCKET','')+'/models/rego_price_gb.joblib' if os.environ.get('USE_S3','false').lower()=='true' else MODEL_PATH

def load_or_train():
    if not os.path.exists(MODEL_PATH):
        train_and_save()
    data = load_bytes('rego_price_gb.joblib')
    if data is not None:
        import io
        return joblib.load(io.BytesIO(data))
    return joblib.load(MODEL_PATH)

def predict(source: str, amount: float, age_days: float) -> float:
    model = load_or_train()
    X = pd.DataFrame([{"source":source, "amount":amount, "age_days":age_days}])
    return float(model.predict(X)[0])
