from app.scrapers.grailed import GrailedScraper
from app.scrapers.fashionphile import FashionphileScraper
from app.scrapers.stdibs import StDibsScraper
from app.scrapers.base import BaseMarketplaceScraper

# Central registry — adding a new source = add one line here
SCRAPER_REGISTRY: dict[str, type[BaseMarketplaceScraper]] = {
    "grailed": GrailedScraper,
    "fashionphile": FashionphileScraper,
    "1stdibs": StDibsScraper,
}

VALID_SOURCES = list(SCRAPER_REGISTRY.keys())
