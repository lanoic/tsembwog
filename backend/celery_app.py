import os
from celery import Celery

broker_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
backend_url = os.getenv("REDIS_URL", "redis://redis:6379/0")

app = Celery("tsembwog", broker=broker_url, backend=backend_url)
app.conf.task_serializer = "json"
app.conf.result_serializer = "json"
app.conf.accept_content = ["json"]
app.conf.task_always_eager = False  # set True for dev sync tasks
