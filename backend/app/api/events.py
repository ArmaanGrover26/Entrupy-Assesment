import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.db.session import get_db
from app.db.models import PriceEvent, Webhook, User
from app.core.deps import get_current_user
from app.schemas.event import (
    PriceEventItem, PriceEventListResponse,
    WebhookCreate, WebhookResponse,
)

router = APIRouter()


@router.get("/events", response_model=PriceEventListResponse)
async def list_events(
    since: Optional[datetime] = Query(None, description="ISO timestamp filter"),
    limit: int = Query(50, ge=1, le=500),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Returns price change events (newest first).
    Consumers can poll using `since` parameter for incremental updates.
    """
    query = select(PriceEvent).order_by(PriceEvent.detected_at.desc())
    if since:
        query = query.where(PriceEvent.detected_at > since)

    count_result = await db.execute(
        select(func.count()).select_from(query.subquery())
    )
    total = count_result.scalar_one()

    result = await db.execute(query.limit(limit))
    events = result.scalars().all()

    return PriceEventListResponse(
        events=[
            PriceEventItem(
                id=str(e.id),
                listing_id=str(e.listing_id),
                old_price=float(e.old_price),
                new_price=float(e.new_price),
                change_pct=float(e.change_pct),
                detected_at=e.detected_at,
                delivered=e.delivered,
            )
            for e in events
        ],
        total=total,
    )


@router.post("/webhooks", response_model=WebhookResponse, status_code=201)
async def register_webhook(
    body: WebhookCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    webhook = Webhook(
        id=uuid.uuid4(),
        user_id=current_user.id,
        url=body.url,
        is_active=True,
    )
    db.add(webhook)
    await db.commit()
    await db.refresh(webhook)

    return WebhookResponse(
        id=str(webhook.id),
        url=webhook.url,
        is_active=webhook.is_active,
        created_at=webhook.created_at,
    )
