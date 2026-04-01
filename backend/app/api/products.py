import math
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.db.session import get_db
from app.db.models import Listing, Product, PriceHistory, User
from app.core.deps import get_current_user
from app.schemas.product import (
    ProductListItem, ProductListResponse,
    ProductDetail, PriceHistoryItem, ProductWithHistory,
)

router = APIRouter()


@router.get("", response_model=ProductListResponse)
async def list_products(
    source: Optional[str] = Query(None, description="grailed | fashionphile | 1stdibs"),
    category: Optional[str] = Query(None),
    brand: Optional[str] = Query(None),
    price_min: Optional[float] = Query(None, ge=0),
    price_max: Optional[float] = Query(None, ge=0),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    offset = (page - 1) * limit

    # Build base query joining listings → products
    query = (
        select(Listing, Product)
        .join(Product, Listing.product_id == Product.id)
        .where(Listing.is_active == True)
    )

    if source:
        query = query.where(Listing.source == source)
    if category:
        query = query.where(Product.category.ilike(f"%{category}%"))
    if brand:
        query = query.where(Product.brand.ilike(f"%{brand}%"))
    if price_min is not None:
        query = query.where(Listing.current_price >= price_min)
    if price_max is not None:
        query = query.where(Listing.current_price <= price_max)

    # Count total
    count_result = await db.execute(
        select(func.count()).select_from(query.subquery())
    )
    total = count_result.scalar_one()

    # Paginate
    result = await db.execute(query.offset(offset).limit(limit))
    rows = result.all()

    items = [
        ProductListItem(
            id=str(listing.id),
            title=listing.title,
            brand=product.brand,
            category=product.category,
            source=listing.source,
            current_price=float(listing.current_price),
            currency=listing.currency,
            condition=listing.condition,
            image_url=listing.image_url,
            url=listing.url,
            last_seen_at=listing.last_seen_at,
        )
        for listing, product in rows
    ]

    return ProductListResponse(
        items=items,
        total=total,
        page=page,
        limit=limit,
        pages=math.ceil(total / limit) if total > 0 else 0,
    )


@router.get("/{listing_id}", response_model=ProductDetail)
async def get_product(
    listing_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Listing, Product)
        .join(Product, Listing.product_id == Product.id)
        .where(Listing.id == listing_id)
    )
    row = result.first()
    if not row:
        raise HTTPException(status_code=404, detail="Product not found")

    listing, product = row
    return ProductDetail(
        id=str(listing.id),
        title=listing.title,
        brand=product.brand,
        category=product.category,
        source=listing.source,
        external_id=listing.external_id,
        current_price=float(listing.current_price),
        currency=listing.currency,
        condition=listing.condition,
        image_url=listing.image_url,
        url=listing.url,
        is_active=listing.is_active,
        last_seen_at=listing.last_seen_at,
        created_at=listing.created_at,
    )


@router.get("/{listing_id}/history", response_model=ProductWithHistory)
async def get_product_history(
    listing_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Listing, Product)
        .join(Product, Listing.product_id == Product.id)
        .where(Listing.id == listing_id)
    )
    row = result.first()
    if not row:
        raise HTTPException(status_code=404, detail="Product not found")

    listing, product = row

    history_result = await db.execute(
        select(PriceHistory)
        .where(PriceHistory.listing_id == listing.id)
        .order_by(PriceHistory.recorded_at.desc())
        .limit(100)
    )
    history = history_result.scalars().all()

    return ProductWithHistory(
        id=str(listing.id),
        title=listing.title,
        brand=product.brand,
        category=product.category,
        source=listing.source,
        external_id=listing.external_id,
        current_price=float(listing.current_price),
        currency=listing.currency,
        condition=listing.condition,
        image_url=listing.image_url,
        url=listing.url,
        is_active=listing.is_active,
        last_seen_at=listing.last_seen_at,
        created_at=listing.created_at,
        price_history=[
            PriceHistoryItem(
                price=float(h.price),
                currency=h.currency,
                recorded_at=h.recorded_at,
            )
            for h in history
        ],
    )
