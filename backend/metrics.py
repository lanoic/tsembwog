from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import APIRouter, Response
from .feature_flags import get_flags

METRICS = {
    "requests_total": Counter("tsembwog_requests_total","Total API requests"),
    "model_trains": Counter("tsembwog_model_trains_total","Model retrains"),
    "rego_predict_latency": Histogram("tsembwog_rego_predict_seconds","REGO price predict latency"),
}

router = APIRouter()

@router.get("/metrics")
def metrics():
    if not get_flags().get("expose_metrics", True):
        return Response(status_code=404)
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
