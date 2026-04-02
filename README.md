# Product Price Monitoring System
### Entrupy Engineering — Intern Assignment

A complete full-stack implementation for tracking luxury marketplace listings, detecting price changes, and displaying live analytics.

## What is included

- Backend REST API with FastAPI
- JWT authentication and token-based sessions
- PostgreSQL data storage with async SQLAlchemy
- Marketplace adapters for Grailed, Fashionphile, and 1stdibs
- Product listing, detail, price history, and analytics endpoints
- Background webhook notification support
- React frontend with Vite, React Router, and React Query

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI, Python 3.9+ |
| Database | PostgreSQL 17 |
| ORM | SQLAlchemy Async |
| Auth | JWT via python-jose + passlib |
| HTTP client | httpx (async) |
| Background tasks | FastAPI BackgroundTasks + tenacity |
| Frontend | React 19, Vite, React Router, React Query |

## Project Structure

```
Entrupy-Assignment/
+-- backend/
¦   +-- app/
¦   ¦   +-- api/          # API routes: auth, products, analytics, refresh, events
¦   ¦   +-- core/         # Config, security, middleware
¦   ¦   +-- db/           # Models, session, migrations, seeding
¦   ¦   +-- scrapers/     # Marketplace adapters and registry
¦   ¦   +-- services/     # Price detection and webhook notifier
¦   +-- tests/            # Pytest coverage for auth and API behavior
¦   +-- requirements.txt
¦   +-- .env.example      # Local runtime env vars
+-- frontend/
¦   +-- src/
¦   ¦   +-- pages/        # Login, Register, Dashboard, Products, ProductDetail, Analytics
¦   ¦   +-- components/   # Navigation, ProtectedRoute
¦   ¦   +-- api/          # HTTP client and auth helper
¦   +-- package.json
¦   +-- vite.config.js
+-- README.md
+-- .gitignore
```

## How to Run

### Prerequisites
- Python 3.9+ installed
- PostgreSQL 17 running locally
- Node.js 18+ installed

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# edit backend/.env to set DATABASE_URL and SECRET_KEY
alembic upgrade head
python -m app.db.seed
uvicorn app.main:app --reload
```

Open API docs at **http://localhost:8000/docs**

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Open the dashboard at **http://localhost:5173**

## Environment variables

Create `backend/.env` from `.env.example` and set:

- `DATABASE_URL` e.g. `postgresql+asyncpg://postgres:abcde@localhost:5432/price_monitor`
- `SECRET_KEY`
- `ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `DEBUG`
- `APP_NAME`

## Main API Endpoints

### Authentication

- `POST /auth/register`
  - Body: `{ "email": "user@example.com", "password": "secret" }`
- `POST /auth/token`
  - Body: `username` and `password` as form data
  - Response: `{ "access_token": "...", "token_type": "bearer" }`

### Products

- `GET /products`
- `GET /products/{id}`
- `GET /products/{id}/history`

### Analytics

- `GET /analytics/summary`

### Refresh

- `POST /refresh`
  - Body: `{ "source": "grailed" }` or omit source for all

### Events / Webhooks

- `GET /events`
- `POST /webhooks`

## Complete Work Summary

This implementation includes:

- user registration and login
- JWT-based authentication
- protected frontend routes for dashboard and product pages
- async database access and schema creation on startup
- product listing, filtering, and pagination
- product detail view with historical price chart
- analytics summary display
- refresh endpoint for marketplace sources
- webhook notification support for price changes

## Recent fixes

- Backend authentication fixed by pinning `bcrypt<5` for compatibility with `passlib[bcrypt]==1.7.4`
- Frontend React Query hooks updated to v5 object-style calls

## Testing

```bash
cd backend
pytest tests/ -v
```

## Ports

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:5173`
- PostgreSQL: `localhost:5432`
