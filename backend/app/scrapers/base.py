from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class ProductIn:
    """Normalized product data from any marketplace scraper."""
    external_id: str
    source: str
    title: str
    brand: str
    category: str
    condition: str
    price: float
    currency: str
    url: str
    image_url: Optional[str] = None


class BaseMarketplaceScraper(ABC):
    """
    All marketplace adapters must implement this interface.
    Swapping mock data for real HTTP scraping = only change this file.
    Adding a new source = new file that inherits this class.
    """

    source_name: str = ""

    @abstractmethod
    async def fetch_products(self) -> list[ProductIn]:
        """Fetch all available products from the marketplace."""
        ...
