from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .config import settings
from . import routers_auth, routers_rego, routers_dsr, routers_btm, routers_ai, routers_admin, ws, seed
from .metrics import router as metrics_router
from . import routers_queue
from .schedulers import scheduler
# Base.metadata.create_all(bind=engine); 
seed.run()
app = FastAPI(title="tsembwog API")
from .middleware import AuditMiddleware, RateLimitMiddleware
import os
try:
    import sentry_sdk
    if os.getenv('SENTRY_DSN'):
        sentry_sdk.init(dsn=os.getenv('SENTRY_DSN'))
except Exception:
    pass

app.add_middleware(CORSMiddleware, allow_origins=[o.strip() for o in settings.CORS_ORIGINS.split(",")], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(routers_auth.router)
app.include_router(routers_rego.router)
app.include_router(routers_dsr.router)
app.include_router(routers_btm.router)
app.include_router(ws.router)

app.include_router(routers_ai.router)
app.include_router(routers_admin.router)
app.include_router(metrics_router)
from . import routers_api_keys
app.include_router(routers_api_keys.router)


app.include_router(routers_admin.router)
app.include_router(metrics_router)

# start scheduler
scheduler.start()

app.add_middleware(AuditMiddleware)
app.add_middleware(RateLimitMiddleware)

app.include_router(routers_queue.router)
