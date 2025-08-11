from .celery_app import app
from .ai.pipeline import train_and_save
from .metrics import METRICS

@app.task
def retrain_rego_model_task():
    path = train_and_save()
    METRICS["model_trains"].inc()
    return {"status":"ok","artifact":path}
