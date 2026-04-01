from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.middleware import UsageTrackingMiddleware
from app.api import auth, products, analytics, refresh, events
from app.db.base import Base
from app.db.session import engine
from app.db import models  # noqa: import all models so Base knows about them


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all tables on startup (code-first schema — no manual SQL needed)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    description="Product Price Monitoring System — Grailed, Fashionphile, 1stDibs",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS — allow React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(UsageTrackingMiddleware)

# Routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
app.include_router(refresh.router, tags=["Data Refresh"])
app.include_router(events.router, tags=["Events & Webhooks"])


@app.get("/", tags=["Health"])
async def root():
    return {"message": "Price Monitor API is running", "docs": "/docs"}


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "healthy"}
