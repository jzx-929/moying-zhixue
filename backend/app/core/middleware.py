import logging
import time
from collections import defaultdict, deque

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

RATE_LIMIT_WINDOW = 60
RATE_LIMIT_MAX = 30


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = (time.time() - start) * 1000

        if request.url.path.startswith("/api"):
            logger.info(
                f"{request.method} {request.url.path} → {response.status_code} ({duration:.0f}ms)"
            )
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests=RATE_LIMIT_MAX, window=RATE_LIMIT_WINDOW):
        super().__init__(app)
        self.max_requests = max_requests
        self.window = window
        self.requests = defaultdict(deque)

    async def dispatch(self, request: Request, call_next):
        if not request.url.path.startswith("/api"):
            return await call_next(request)

        client = request.client.host if request.client else "unknown"
        now = time.time()
        q = self.requests[client]
        while q and q[0] < now - self.window:
            q.popleft()

        if len(q) >= self.max_requests:
            return Response(
                content='{"code":429,"message":"请求过于频繁，请稍后再试"}',
                status_code=429,
                media_type="application/json",
            )

        q.append(now)
        return await call_next(request)
