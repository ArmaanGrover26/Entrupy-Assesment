import uuid
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


SKIP_PATHS = {"/docs", "/redoc", "/openapi.json", "/", "/health"}


class UsageTrackingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        if request.url.path in SKIP_PATHS:
            return await call_next(request)

        response = await call_next(request)

        # Fire-and-forget usage log — never blocks the response
        try:
            from app.db.session import AsyncSessionLocal
            from app.db.models import ApiUsage

            async def _log():
                async with AsyncSessionLocal() as db:
                    usage = ApiUsage(
                        id=uuid.uuid4(),
                        endpoint=request.url.path,
                        method=request.method,
                        status_code=response.status_code,
                    )
                    db.add(usage)
                    await db.commit()

            import asyncio
            asyncio.create_task(_log())
        except Exception:
            pass  # Logging must never break a request

        return response
