from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.db.session import get_db
from app.db.models import Listing, Product, PriceEvent, User
from app.core.deps import get_current_user

router = APIRouter()


@router.get("/summary")
async def get_analytics_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Totals by source
    source_result = await db.execute(
        select(Listing.source, func.count(Listing.id))
        .where(Listing.is_active == True)
        .group_by(Listing.source)
    )
    totals_by_source = {row[0]: row[1] for row in source_result}

    # Average price by category (join listings → products)
    cat_result = await db.execute(
        select(Product.category, func.avg(Listing.current_price))
        .join(Listing, Product.id == Listing.product_id)
        .where(Listing.is_active == True)
        .group_by(Product.category)
    )
    avg_price_by_category = {
        row[0]: round(float(row[1]), 2) for row in cat_result
    }

    # Total active listings
    total = await db.scalar(
        select(func.count(Listing.id)).where(Listing.is_active == True)
    )

    # Price changes in last 24 hours
    cutoff = datetime.utcnow() - timedelta(hours=24)
    recent_changes = await db.scalar(
        select(func.count(PriceEvent.id))
        .where(PriceEvent.detected_at >= cutoff)
    )

    # Price changes in last 7 days
    cutoff_week = datetime.utcnow() - timedelta(days=7)
    weekly_changes = await db.scalar(
        select(func.count(PriceEvent.id))
        .where(PriceEvent.detected_at >= cutoff_week)
    )

    # Most recent refresh timestamp
    last_refresh = await db.scalar(select(func.max(Listing.last_seen_at)))

    # Min / max / avg price overall
    price_stats = await db.execute(
        select(
            func.min(Listing.current_price),
            func.max(Listing.current_price),
            func.avg(Listing.current_price),
        ).where(Listing.is_active == True)
    )
    stats_row = price_stats.one()

    return {
        "totals_by_source": totals_by_source,
        "avg_price_by_category": avg_price_by_category,
        "total_active_listings": total,
        "price_changes_last_24h": recent_changes,
        "price_changes_last_7d": weekly_changes,
        "last_refresh": last_refresh,
        "price_stats": {
            "min": float(stats_row[0]) if stats_row[0] else 0,
            "max": float(stats_row[1]) if stats_row[1] else 0,
            "avg": round(float(stats_row[2]), 2) if stats_row[2] else 0,
        },
    }
