"""
Seed script — populates the database with realistic sample data from all 3 marketplaces.
Run: python -m app.db.seed
"""
import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.db.session import AsyncSessionLocal
from app.db.base import Base
from app.db.session import engine
from app.db import models  # noqa
from app.scrapers.registry import SCRAPER_REGISTRY
from app.api.refresh import trigger_refresh
import uuid
from sqlalchemy import select
from app.db.models import Product, Listing
from app.services.price_detector import upsert_listing


async def seed():
    print("Creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("Seeding data from all 3 marketplaces...")
    async with AsyncSessionLocal() as db:
        for source_name, scraper_class in SCRAPER_REGISTRY.items():
            scraper = scraper_class()
            products_data = await scraper.fetch_products()
            count = 0
            for data in products_data:
                # Find or create canonical product
                result = await db.execute(
                    select(Product).where(
                        Product.brand == data.brand,
                        Product.category == data.category,
                        Product.canonical_title == data.title,
                    )
                )
                product = result.scalar_one_or_none()
                if not product:
                    product = Product(
                        id=uuid.uuid4(),
                        brand=data.brand,
                        category=data.category,
                        canonical_title=data.title,
                    )
                    db.add(product)
                    await db.flush()

                await upsert_listing(db, product.id, data)
                count += 1

            print(f"  ✓ {source_name}: {count} listings seeded")

    print("Seed complete!")


if __name__ == "__main__":
    asyncio.run(seed())
