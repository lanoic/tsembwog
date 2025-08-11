from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .ai.pipeline import train_and_save
from .feature_flags import get_flags
from .metrics import METRICS

scheduler = AsyncIOScheduler()

@scheduler.scheduled_job("cron", hour=3, minute=0)  # daily retrain at 03:00
def retrain_rego_price():
    flags = get_flags()
    if flags.get("use_gb_rego_price_model", True):
        path = train_and_save()
        METRICS["model_trains"].inc()
        print(f"[scheduler] retrained model saved at {path}")
