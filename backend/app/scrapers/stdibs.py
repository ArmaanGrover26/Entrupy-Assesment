import asyncio
import random
from app.scrapers.base import BaseMarketplaceScraper, ProductIn

_STDIBS_CATALOG = [
    {"external_id": "st-001", "title": "Cartier Love Bracelet 18K Yellow Gold", "brand": "Cartier", "category": "jewelry", "condition": "Excellent", "base_price": 5200.0, "url": "https://1stdibs.com/jewelry/st-001", "image_url": "https://images.1stdibs.com/st-001.jpg"},
    {"external_id": "st-002", "title": "Rolex Datejust 36 Stainless Steel White Dial", "brand": "Rolex", "category": "watches", "condition": "Very Good", "base_price": 8500.0, "url": "https://1stdibs.com/watches/st-002", "image_url": "https://images.1stdibs.com/st-002.jpg"},
    {"external_id": "st-003", "title": "Tiffany & Co. Diamond Solitaire Ring Platinum", "brand": "Tiffany & Co.", "category": "jewelry", "condition": "Excellent", "base_price": 4800.0, "url": "https://1stdibs.com/jewelry/st-003", "image_url": "https://images.1stdibs.com/st-003.jpg"},
    {"external_id": "st-004", "title": "Omega Constellation Vintage 1960s Gold", "brand": "Omega", "category": "watches", "condition": "Good", "base_price": 2400.0, "url": "https://1stdibs.com/watches/st-004", "image_url": "https://images.1stdibs.com/st-004.jpg"},
    {"external_id": "st-005", "title": "Van Cleef & Arpels Alhambra Bracelet", "brand": "Van Cleef & Arpels", "category": "jewelry", "condition": "Excellent", "base_price": 9500.0, "url": "https://1stdibs.com/jewelry/st-005", "image_url": "https://images.1stdibs.com/st-005.jpg"},
    {"external_id": "st-006", "title": "Art Deco Diamond Drop Earrings Platinum", "brand": "Antique", "category": "jewelry", "condition": "Good", "base_price": 6200.0, "url": "https://1stdibs.com/jewelry/st-006", "image_url": "https://images.1stdibs.com/st-006.jpg"},
    {"external_id": "st-007", "title": "Vintage Hermès Kelly 32 Togo Gold HW", "brand": "Hermès", "category": "bags", "condition": "Very Good", "base_price": 12000.0, "url": "https://1stdibs.com/fashion/st-007", "image_url": "https://images.1stdibs.com/st-007.jpg"},
    {"external_id": "st-008", "title": "Patek Philippe Calatrava 18K White Gold", "brand": "Patek Philippe", "category": "watches", "condition": "Excellent", "base_price": 18500.0, "url": "https://1stdibs.com/watches/st-008", "image_url": "https://images.1stdibs.com/st-008.jpg"},
    {"external_id": "st-009", "title": "Bulgari Serpenti Tubogas Bracelet Watch", "brand": "Bulgari", "category": "watches", "condition": "Very Good", "base_price": 7200.0, "url": "https://1stdibs.com/watches/st-009", "image_url": "https://images.1stdibs.com/st-009.jpg"},
    {"external_id": "st-010", "title": "Mid-Century Modern Eames Lounge Chair", "brand": "Herman Miller", "category": "furniture", "condition": "Good", "base_price": 3600.0, "url": "https://1stdibs.com/furniture/st-010", "image_url": "https://images.1stdibs.com/st-010.jpg"},
]


class StDibsScraper(BaseMarketplaceScraper):
    """Mock adapter for 1stDibs — high-end jewelry, watches, and antiques."""

    source_name = "1stdibs"

    async def fetch_products(self) -> list[ProductIn]:
        await asyncio.sleep(0.1)
        products = []
        for item in _STDIBS_CATALOG:
            fluctuation = random.uniform(-0.05, 0.05)
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
