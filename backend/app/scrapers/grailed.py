import asyncio
import random
from app.scrapers.base import BaseMarketplaceScraper, ProductIn

# Base prices — realistic streetwear/designer market values
_GRAILED_CATALOG = [
    {"external_id": "gr-001", "title": "Supreme Box Logo Hoodie FW22", "brand": "Supreme", "category": "outerwear", "condition": "Good", "base_price": 380.0, "url": "https://grailed.com/listings/gr-001", "image_url": "https://images.grailed.com/gr-001.jpg"},
    {"external_id": "gr-002", "title": "Off-White Industrial Belt Yellow", "brand": "Off-White", "category": "accessories", "condition": "Very Good", "base_price": 245.0, "url": "https://grailed.com/listings/gr-002", "image_url": "https://images.grailed.com/gr-002.jpg"},
    {"external_id": "gr-003", "title": "Balenciaga Triple S Sneakers Grey", "brand": "Balenciaga", "category": "shoes", "condition": "Good", "base_price": 620.0, "url": "https://grailed.com/listings/gr-003", "image_url": "https://images.grailed.com/gr-003.jpg"},
    {"external_id": "gr-004", "title": "Yeezy Boost 350 V2 Zebra", "brand": "Adidas Yeezy", "category": "shoes", "condition": "Excellent", "base_price": 390.0, "url": "https://grailed.com/listings/gr-004", "image_url": "https://images.grailed.com/gr-004.jpg"},
    {"external_id": "gr-005", "title": "Palace Tri-Ferg Hoodie Navy", "brand": "Palace", "category": "outerwear", "condition": "Good", "base_price": 280.0, "url": "https://grailed.com/listings/gr-005", "image_url": "https://images.grailed.com/gr-005.jpg"},
    {"external_id": "gr-006", "title": "Fear of God Essentials Hoodie", "brand": "Fear of God", "category": "outerwear", "condition": "Like New", "base_price": 170.0, "url": "https://grailed.com/listings/gr-006", "image_url": "https://images.grailed.com/gr-006.jpg"},
    {"external_id": "gr-007", "title": "Jordan 1 Retro High Bred Toe", "brand": "Nike Jordan", "category": "shoes", "condition": "Very Good", "base_price": 340.0, "url": "https://grailed.com/listings/gr-007", "image_url": "https://images.grailed.com/gr-007.jpg"},
    {"external_id": "gr-008", "title": "Stüssy World Tour Tee White", "brand": "Stüssy", "category": "tops", "condition": "Good", "base_price": 130.0, "url": "https://grailed.com/listings/gr-008", "image_url": "https://images.grailed.com/gr-008.jpg"},
    {"external_id": "gr-009", "title": "Comme des Garçons PLAY Cardigan", "brand": "Comme des Garçons", "category": "outerwear", "condition": "Excellent", "base_price": 310.0, "url": "https://grailed.com/listings/gr-009", "image_url": "https://images.grailed.com/gr-009.jpg"},
    {"external_id": "gr-010", "title": "Acne Studios Oversized Coat Grey", "brand": "Acne Studios", "category": "outerwear", "condition": "Very Good", "base_price": 480.0, "url": "https://grailed.com/listings/gr-010", "image_url": "https://images.grailed.com/gr-010.jpg"},
]


class GrailedScraper(BaseMarketplaceScraper):
    """
    Mock adapter for Grailed marketplace.
    Simulates realistic price fluctuations on each fetch (±8%)
    so that price change detection actually fires.
    """

    source_name = "grailed"

    async def fetch_products(self) -> list[ProductIn]:
        await asyncio.sleep(0.1)  # simulate network latency
        products = []
        for item in _GRAILED_CATALOG:
            # ±8% price fluctuation to simulate market activity
            fluctuation = random.uniform(-0.08, 0.08)
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
