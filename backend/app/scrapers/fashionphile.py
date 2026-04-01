import asyncio
import random
from app.scrapers.base import BaseMarketplaceScraper, ProductIn

_FASHIONPHILE_CATALOG = [
    {"external_id": "fp-001", "title": "Louis Vuitton Neverfull MM Monogram", "brand": "Louis Vuitton", "category": "bags", "condition": "Very Good", "base_price": 1200.0, "url": "https://fashionphile.com/p/fp-001", "image_url": "https://images.fashionphile.com/fp-001.jpg"},
    {"external_id": "fp-002", "title": "Chanel Classic Flap Medium Caviar", "brand": "Chanel", "category": "bags", "condition": "Excellent", "base_price": 6500.0, "url": "https://fashionphile.com/p/fp-002", "image_url": "https://images.fashionphile.com/fp-002.jpg"},
    {"external_id": "fp-003", "title": "Gucci GG Marmont Shoulder Bag", "brand": "Gucci", "category": "bags", "condition": "Good", "base_price": 1450.0, "url": "https://fashionphile.com/p/fp-003", "image_url": "https://images.fashionphile.com/fp-003.jpg"},
    {"external_id": "fp-004", "title": "Prada Re-Edition 2005 Nylon", "brand": "Prada", "category": "bags", "condition": "Like New", "base_price": 1100.0, "url": "https://fashionphile.com/p/fp-004", "image_url": "https://images.fashionphile.com/fp-004.jpg"},
    {"external_id": "fp-005", "title": "Hermès Evelyne PM Taurillon", "brand": "Hermès", "category": "bags", "condition": "Excellent", "base_price": 3200.0, "url": "https://fashionphile.com/p/fp-005", "image_url": "https://images.fashionphile.com/fp-005.jpg"},
    {"external_id": "fp-006", "title": "Bottega Veneta The Pouch Clutch", "brand": "Bottega Veneta", "category": "bags", "condition": "Like New", "base_price": 1800.0, "url": "https://fashionphile.com/p/fp-006", "image_url": "https://images.fashionphile.com/fp-006.jpg"},
    {"external_id": "fp-007", "title": "Celine Box Bag Small Smooth Leather", "brand": "Celine", "category": "bags", "condition": "Very Good", "base_price": 2100.0, "url": "https://fashionphile.com/p/fp-007", "image_url": "https://images.fashionphile.com/fp-007.jpg"},
    {"external_id": "fp-008", "title": "MCM Stark Backpack Visetos Medium", "brand": "MCM", "category": "bags", "condition": "Good", "base_price": 680.0, "url": "https://fashionphile.com/p/fp-008", "image_url": "https://images.fashionphile.com/fp-008.jpg"},
    {"external_id": "fp-009", "title": "Dior Lady Dior Mini Cannage", "brand": "Dior", "category": "bags", "condition": "Excellent", "base_price": 3800.0, "url": "https://fashionphile.com/p/fp-009", "image_url": "https://images.fashionphile.com/fp-009.jpg"},
    {"external_id": "fp-010", "title": "Saint Laurent Loulou Puffer Small", "brand": "Saint Laurent", "category": "bags", "condition": "Very Good", "base_price": 1350.0, "url": "https://fashionphile.com/p/fp-010", "image_url": "https://images.fashionphile.com/fp-010.jpg"},
]


class FashionphileScraper(BaseMarketplaceScraper):
    """Mock adapter for Fashionphile — luxury handbags and accessories."""

    source_name = "fashionphile"

    async def fetch_products(self) -> list[ProductIn]:
        await asyncio.sleep(0.1)
        products = []
        for item in _FASHIONPHILE_CATALOG:
            fluctuation = random.uniform(-0.06, 0.06)
            price = round(item["base_price"] * (1 + fluctuation), 2)
            products.append(
                ProductIn(
                    external_id=item["external_id"],
                    source=self.source_name,
                    title=item["title"],
                    brand=item["brand"],
                    category=item["category"],
                    condition=item["condition"],
                    price=price,
                    currency="USD",
                    url=item["url"],
                    image_url=item["image_url"],
                )
            )
        return products
