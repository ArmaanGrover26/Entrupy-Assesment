import httpx
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models import Webhook, PriceEvent

"""notifications"""

async def deliver_price_event(db: AsyncSession, event: PriceEvent) -> None:
    """
    Deliver a price event to all registered webhooks.
    Runs as a FastAPI BackgroundTask — never blocks the refresh endpoint.

    Strategy:
    - Fetch all active webhooks
    - For each, attempt delivery with exponential backoff (up to 3 retries)
    - Update delivered/retry_count regardless of outcome
    - Event record is never deleted — full audit trail maintained
    """
    result = await db.execute(select(Webhook).where(Webhook.is_active == True))
    webhooks = result.scalars().all()

    if not webhooks:
        return

    payload = {
        "event": "price_change",
        "listing_id": str(event.listing_id),
        "old_price": float(event.old_price),
        "new_price": float(event.new_price),
        "change_pct": float(event.change_pct),
        "detected_at": event.detected_at.isoformat(),
    }

    all_delivered = True
    for webhook in webhooks:
        try:
            await _send_with_retry(webhook.url, payload)
        except Exception:
            event.retry_count += 1
            all_delivered = False

    if all_delivered:
        event.delivered = True

    await db.commit()


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=8),
    retry=retry_if_exception_type(httpx.HTTPError),
    reraise=True,
)
async def _send_with_retry(url: str, payload: dict) -> None:
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
