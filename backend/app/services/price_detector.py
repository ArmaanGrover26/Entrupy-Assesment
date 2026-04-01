import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models import Listing, PriceHistory, PriceEvent
from app.scrapers.base import ProductIn


async def upsert_listing(
    db: AsyncSession,
    product_id: uuid.UUID,
    data: ProductIn,
) -> tuple[Listing, bool, "PriceEvent | None"]:
    """
    Insert or update a listing and detect price changes.

    Returns:
        (listing, is_new, price_event_or_none)
    """
    result = await db.execute(
        select(Listing).where(
            Listing.external_id == data.external_id,
            Listing.source == data.source,
        )
    )
    existing: Listing | None = result.scalar_one_or_none()

    if existing is None:
        # New listing — insert and record initial price history
        listing = Listing(
            id=uuid.uuid4(),
            product_id=product_id,
            source=data.source,
            external_id=data.external_id,
            title=data.title,
            condition=data.condition,
            current_price=Decimal(str(data.price)),
            currency=data.currency,
            url=data.url,
            image_url=data.image_url,
            is_active=True,
            last_seen_at=datetime.utcnow(),
        )
        db.add(listing)
        await db.flush()  # get the ID

        history = PriceHistory(
            id=uuid.uuid4(),
            listing_id=listing.id,
            price=listing.current_price,
            currency=listing.currency,
            recorded_at=datetime.utcnow(),
        )
        db.add(history)
        await db.commit()
        await db.refresh(listing)
        return listing, True, None

    # Existing listing — check for price change
    new_price = Decimal(str(data.price))
    old_price = existing.current_price
    event = None

    # Always record snapshot in history
    history = PriceHistory(
        id=uuid.uuid4(),
        listing_id=existing.id,
        price=new_price,
        currency=data.currency,
        recorded_at=datetime.utcnow(),
    )
    db.add(history)

    if abs(float(old_price) - float(new_price)) >= 0.01:
        change_pct = ((float(new_price) - float(old_price)) / float(old_price)) * 100
        event = PriceEvent(
            id=uuid.uuid4(),
            listing_id=existing.id,
            old_price=old_price,
            new_price=new_price,
            change_pct=round(change_pct, 4),
            detected_at=datetime.utcnow(),
            delivered=False,
            retry_count=0,
        )
        db.add(event)
        existing.current_price = new_price

    existing.last_seen_at = datetime.utcnow()
    existing.is_active = True

    await db.commit()
    if event:
        await db.refresh(event)
    return existing, False, event
