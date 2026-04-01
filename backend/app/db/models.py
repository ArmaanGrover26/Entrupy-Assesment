import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean, Column, DateTime, ForeignKey,
    Integer, Numeric, String, Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    api_key = Column(String(64), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    api_usage = relationship("ApiUsage", back_populates="user")
    webhooks = relationship("Webhook", back_populates="user")


class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brand = Column(String(255), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    canonical_title = Column(String(500), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    listings = relationship("Listing", back_populates="product")


class Listing(Base):
    """One row per marketplace listing. Same product can appear on multiple platforms."""
    __tablename__ = "listings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    source = Column(String(50), nullable=False, index=True)       # grailed | fashionphile | 1stdibs
    external_id = Column(String(255), nullable=False)              # marketplace's own ID
    title = Column(String(500), nullable=False)
    condition = Column(String(100))
    current_price = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(10), default="USD")
    url = Column(Text)
    image_url = Column(Text)
    is_active = Column(Boolean, default=True)
    last_seen_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    product = relationship("Product", back_populates="listings")
    price_history = relationship("PriceHistory", back_populates="listing")
    price_events = relationship("PriceEvent", back_populates="listing")


class PriceHistory(Base):
    """
    Immutable log of every price snapshot.
    Index on (listing_id, recorded_at DESC) for fast history queries.
    At scale: partition by RANGE(recorded_at) monthly.
    """
    __tablename__ = "price_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    listing_id = Column(UUID(as_uuid=True), ForeignKey("listings.id"), nullable=False, index=True)
    price = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(10), default="USD")
    recorded_at = Column(DateTime(timezone=True), default=datetime.utcnow, index=True)

    listing = relationship("Listing", back_populates="price_history")


class PriceEvent(Base):
    """Fired when a listing's price changes. Used for notifications."""
    __tablename__ = "price_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    listing_id = Column(UUID(as_uuid=True), ForeignKey("listings.id"), nullable=False, index=True)
    old_price = Column(Numeric(12, 2), nullable=False)
    new_price = Column(Numeric(12, 2), nullable=False)
    change_pct = Column(Numeric(8, 4), nullable=False)
    detected_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    delivered = Column(Boolean, default=False)
    retry_count = Column(Integer, default=0)

    listing = relationship("Listing", back_populates="price_events")


class ApiUsage(Base):
    """Every API request is logged here for usage tracking."""
    __tablename__ = "api_usage"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    endpoint = Column(String(255), nullable=False)
    method = Column(String(10), nullable=False)
    status_code = Column(Integer)
    requested_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    user = relationship("User", back_populates="api_usage")


class Webhook(Base):
    """Registered webhook endpoints for price change notifications."""
    __tablename__ = "webhooks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    url = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    user = relationship("User", back_populates="webhooks")
