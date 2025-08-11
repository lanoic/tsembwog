from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
import time
from .deps import get_current_user
from .feature_flags import get_flags
from .metrics import METRICS
from .ai.pipeline import predict as gb_predict
from .ai.intelligence import DSRRecommender  # keep greedy as fallback
from .ai.optimization import lp_allocate_dsr, mpc_schedule

router = APIRouter(prefix="/ai", tags=["ai"])
greedy = DSRRecommender()

class RegoPriceIn(BaseModel):
    source: str
    amount_mwh: float
    age_days: float

@router.post("/rego/price_predict")
def rego_price(req: RegoPriceIn, user=Depends(get_current_user)):
    start = time.perf_counter()
    flags = get_flags()
    if flags.get("use_gb_rego_price_model", True):
        price = gb_predict(req.source, req.amount_mwh, req.age_days)
    else:
        # basic heuristic
        base = 6.5 + (0.7 if "Solar" in req.source else 0.0) + (0.3 if "Wind" in req.source else 0.0)
        price = base + 0.004*req.amount_mwh - 0.0015*req.age_days
    METRICS["requests_total"].inc()
    METRICS["rego_predict_latency"].observe(time.perf_counter()-start)
    return {"price_per_mwh": round(float(price), 3)}

@router.get("/dsr/recommend")
def dsr_recommend(event_id: int, user=Depends(get_current_user)):
    flags = get_flags()
    if flags.get("enable_dsr_lp_optimizer", True):
        return lp_allocate_dsr(event_id)
    return greedy.recommend(event_id)

class BtmOptIn(BaseModel):
    device_id: int
    prices: List[float]
    p_low: float | None = None
    p_high: float | None = None

@router.post("/btm/optimize")
def btm_optimize(req: BtmOptIn, user=Depends(get_current_user)):
    flags = get_flags()
    if flags.get("enable_btm_mpc", True):
        return mpc_schedule(req.device_id, req.prices)
    # fallback: threshold policy via basic optimizer in intelligence
    from .ai.intelligence import BTMOptimizer
    return BTMOptimizer().optimize(req.device_id, req.prices, req.p_low or 0.12, req.p_high or 0.25)
