import uuid
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.db.models import User, Product, Listing
from app.core.deps import get_current_user
from app.scrapers.registry import SCRAPER_REGISTRY, VALID_SOURCES
from app.services.price_detector import upsert_listing
from app.services.notifier import deliver_price_event
from app.schemas.product import RefreshRequest, RefreshResponse

router = APIRouter()


@router.post("/refresh", response_model=RefreshResponse)
async def trigger_refresh(
    body: RefreshRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Trigger a data refresh for one or all marketplace sources.
    Price changes are detected automatically and events are fired asynchronously.
    """
    if body.source and body.source not in VALID_SOURCES:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown source '{body.source}'. Valid: {VALID_SOURCES}",
        )

    sources = [body.source] if body.source else VALID_SOURCES
    total_updated = 0
    total_new = 0

    for source_name in sources:
        scraper = SCRAPER_REGISTRY[source_name]()
        products = await scraper.fetch_products()

        for data in products:
            # Find or create canonical product record
            product_result = await db.execute(
                select(Product).where(
                    Product.brand == data.brand,
                    Product.category == data.category,
                    Product.canonical_title == data.title,
                )
            )
            product = product_result.scalar_one_or_none()

            if not product:
                product = Product(
                    id=uuid.uuid4(),
                    brand=data.brand,
                    category=data.category,
                    canonical_title=data.title,
                )
                db.add(product)
                await db.flush()

            _, is_new, event = await upsert_listing(db, product.id, data)

            if is_new:
                total_new += 1
            else:
                total_updated += 1

            # Deliver price change events in background — never blocks this response
            if event:
                background_tasks.add_task(deliver_price_event, db, event)

    return RefreshResponse(
        message="Refresh complete",
        products_updated=total_updated,
        products_new=total_new,
        sources_refreshed=sources,
    )
