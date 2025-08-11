import time
from collections import defaultdict, deque
from typing import Deque
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, PlainTextResponse
import os, threading

AUDIT_PATH = os.environ.get("AUDIT_LOG_PATH", "/app/logs/audit.log")
os.makedirs(os.path.dirname(AUDIT_PATH), exist_ok=True)
_lock = threading.Lock()

def append_audit(line: str):
    with _lock:
        with open(AUDIT_PATH, "a") as f:
            f.write(line + "\n")

class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        resp = await call_next(request)
        dur = time.time() - start
        user = request.headers.get("authorization","")[:20]
        append_audit(f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} {request.client.host} {request.method} {request.url.path} {resp.status_code} {dur:.3f} auth={bool(user)}")
        return resp

class RateLimitMiddleware(BaseHTTPMiddleware):
    # very simple per-IP sliding window limiter
    hits: dict[str, Deque[float]] = defaultdict(lambda: deque())
    def __init__(self, app, per_minute: int = 100):
        super().__init__(app)
        self.limit = per_minute

    async def dispatch(self, request: Request, call_next):
        ip = request.client.host or "unknown"
        now = time.time()
        dq = self.hits[ip]
        # purge older than 60s
        while dq and now - dq[0] > 60:
            dq.popleft()
        if len(dq) >= self.limit:
            return PlainTextResponse("Rate limit exceeded", status_code=429)
        dq.append(now)
        return await call_next(request)
