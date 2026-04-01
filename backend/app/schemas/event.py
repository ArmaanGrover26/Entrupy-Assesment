from pydantic import BaseModel, HttpUrl
from typing import List
from datetime import datetime


class PriceEventItem(BaseModel):
    id: str
    listing_id: str
    old_price: float
    new_price: float
    change_pct: float
    detected_at: datetime
    delivered: bool

    model_config = {"from_attributes": True}


class PriceEventListResponse(BaseModel):
    events: List[PriceEventItem]
    total: int


class WebhookCreate(BaseModel):
    url: str


class WebhookResponse(BaseModel):
    id: str
    url: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
