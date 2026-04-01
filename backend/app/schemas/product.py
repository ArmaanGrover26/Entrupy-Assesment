from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ProductListItem(BaseModel):
    id: str
    title: str
    brand: str
    category: str
    source: str
    current_price: float
    currency: str
    condition: Optional[str] = None
    image_url: Optional[str] = None
    url: Optional[str] = None
    last_seen_at: datetime

    model_config = {"from_attributes": True}


class ProductListResponse(BaseModel):
    items: List[ProductListItem]
    total: int
    page: int
    limit: int
    pages: int


class ProductDetail(ProductListItem):
    external_id: str
    is_active: bool
    created_at: datetime


class PriceHistoryItem(BaseModel):
    price: float
    currency: str
    recorded_at: datetime

    model_config = {"from_attributes": True}


class ProductWithHistory(ProductDetail):
    price_history: List[PriceHistoryItem] = []


class RefreshRequest(BaseModel):
    source: Optional[str] = None  # grailed | fashionphile | 1stdibs | None = all


class RefreshResponse(BaseModel):
    message: str
    products_updated: int
    products_new: int
    sources_refreshed: List[str]
