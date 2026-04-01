# Product Price Monitoring System
### Entrupy Engineering — Intern Assignment

A full-stack system that collects product data from luxury marketplaces (Grailed, Fashionphile, 1stdibs), tracks price changes in real time, serves a REST API, notifies on price changes, and displays a live dashboard.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python 3.9+) |
| Database | PostgreSQL 17 |
| Migrations | Alembic (code-first, no manual SQL) |
| Frontend | React + Vite |
| Auth | JWT (python-jose + passlib) |
| HTTP Client | httpx (async) |
| Notifications | Event log + BackgroundTask webhooks |

---

## Project Structure

```
Entrupy-Assignment/
├── backend/
│   ├── app/
│   │   ├── api/          # Route handlers (auth, products, analytics, events)
│   │   ├── core/         # Config, security, middleware
│   │   ├── db/           # SQLAlchemy models, session, Alembic
│   │   ├── scrapers/     # Marketplace adapters (Grailed, Fashionphile, 1stdibs)
│   │   └── services/     # Price detection, webhook notifier
│   ├── tests/            # 8+ pytest tests
│   ├── alembic/          # Migration files (version-controlled)
│   ├── requirements.txt
│   └── .env              # Local secrets (not committed)
├── frontend/
│   ├── src/
│   │   ├── pages/        # Dashboard, ProductList, ProductDetail
│   │   ├── components/   # Reusable UI components
│   │   └── hooks/        # React Query hooks
│   └── package.json
├── README.md
└── .gitignore
```

---

## How to Run

### Prerequisites
- Python 3.9+
- PostgreSQL 17 (running locally)
- Node.js 18+

### 1. Clone the repo
```bash
git clone https://github.com/ArmaanGrover26/Entrupy-Assignment.git
cd Entrupy-Assignment
```

### 2. Backend Setup
```bash
cd backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
copy .env.example .env
# Edit .env with your PostgreSQL credentials

# Run migrations (creates all tables automatically)
alembic upgrade head

# Seed sample data
python -m app.db.seed

# Start the API server (port 8000)
uvicorn app.main:app --reload
```

API docs available at: **http://localhost:8000/docs**

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Dashboard available at: **http://localhost:5173**

---

## API Documentation

All protected endpoints require a JWT Bearer token.

### Authentication
```
POST /auth/register
Body: { "email": "user@example.com", "password": "secret" }

POST /auth/token
Body: { "username": "user@example.com", "password": "secret" }
Response: { "access_token": "...", "token_type": "bearer" }
```

### Products
```
GET /products
Query params: source, category, price_min, price_max, page, limit
Response: { "items": [...], "total": 120, "page": 1 }

GET /products/{id}
Response: { product details + current listing info }

GET /products/{id}/history
Response: { "history": [{ "price": 450.00, "recorded_at": "..." }] }
```

### Data Refresh
```
POST /refresh
Body: { "source": "grailed" }   # or omit for all sources
Response: { "message": "Refresh triggered", "products_updated": 12 }
```

### Analytics
```
GET /analytics/summary
Response: {
  "totals_by_source": { "grailed": 45, "fashionphile": 38, "1stdibs": 27 },
  "avg_price_by_category": { "bags": 1250.00, "shoes": 480.00 },
  "recent_price_changes": 7,
  "last_refresh": "2024-01-15T10:30:00Z"
}
```

### Price Events
```
GET /events
Query params: since (ISO timestamp), limit
Response: { "events": [{ "listing_id": "...", "old_price": 400, "new_price": 350, ... }] }

POST /webhooks
Body: { "url": "https://your-endpoint.com/hook" }
```

---

## Design Decisions

### 1. How does price history scale to millions of rows?

The `price_history` table uses **PostgreSQL range partitioning** by `recorded_at` (monthly partitions). Each month's data lives in a separate physical partition, so queries like "get history for last 30 days" only scan one partition instead of the full table.

Additionally, a composite index on `(listing_id, recorded_at DESC)` means fetching a product's history is an index-only scan — O(log n) regardless of table size.

For even larger scale, old partitions can be archived to cheap storage (e.g., S3 via `pg_partman`) with zero changes to application code.

### 2. Why event log over webhooks or message queues?

Three options were considered:

| Approach | Pros | Cons |
|---|---|---|
| **Event log (chosen)** | No lost events, queryable, no infra | Requires polling |
| Pure webhooks | Push-based | Delivery failures = lost events |
| Redis/Celery queue | True async, scalable | Adds infrastructure complexity for a placement project |

The event log approach means price changes are persisted in `price_events` first — always. Webhook delivery happens asynchronously via FastAPI `BackgroundTasks` with exponential backoff retry (`tenacity`). This satisfies the assignment requirement: "reliable, handle delivery failures, don't block the fetch process."

### 3. How would you extend to 100+ data sources?

The scraper layer uses a **pluggable adapter pattern**:

```python
class BaseMarketplaceScraper:
    async def fetch_products(self) -> list[ProductIn]: ...

class GrailedScraper(BaseMarketplaceScraper): ...
class FashionphileScraper(BaseMarketplaceScraper): ...
```

Adding a new source = create one new file inheriting `BaseMarketplaceScraper` + register in a `SOURCE_REGISTRY` dict. Zero changes to the refresh API, price detection logic, or database schema.

At 100+ sources, you'd add a task queue (Celery + Redis) to run scrapers in parallel with rate limiting — the adapter interface doesn't change.

---

## Known Limitations

- **Mock data only**: Marketplace adapters return realistic simulated data. Real scraping would require handling CAPTCHAs, rate limiting, and HTML parsing — not implemented intentionally.
- **No OAuth**: JWT is implemented but no refresh token rotation. Production would use short-lived access + long-lived refresh tokens.
- **Partitioning is pre-configured**: Monthly partitions are created for the current year. A `pg_partman` job would be needed in production to auto-create future partitions.
- **Single webhook delivery attempt per background task**: Retry logic uses in-process tenacity; a production system would use a persistent job queue.
- **No pagination on `/events`**: Cursor-based pagination would be added for high-volume consumers.

---

## Running Tests

```bash
cd backend
pytest tests/ -v
```

Expected: 8+ tests covering auth, products, filtering, price detection edge cases.

---

## Ports Used
- Backend API: `http://localhost:8000`
- Frontend: `http://localhost:5173`
- PostgreSQL: `localhost:5432`
