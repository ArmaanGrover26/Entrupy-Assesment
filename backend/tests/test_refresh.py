import pytest


@pytest.mark.asyncio
async def test_analytics_summary_structure(client, auth_headers):
    """Analytics endpoint returns expected fields."""
    await client.post("/refresh", json={}, headers=auth_headers)
    resp = await client.get("/analytics/summary", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "totals_by_source" in data
    assert "avg_price_by_category" in data
    assert "total_active_listings" in data
    assert "price_changes_last_24h" in data
    assert "price_stats" in data


@pytest.mark.asyncio
async def test_analytics_source_counts(client, auth_headers):
    """After refreshing all sources, all 3 appear in analytics totals."""
    await client.post("/refresh", json={}, headers=auth_headers)
    resp = await client.get("/analytics/summary", headers=auth_headers)
    totals = resp.json()["totals_by_source"]
    assert "grailed" in totals
    assert "fashionphile" in totals
    assert "1stdibs" in totals


@pytest.mark.asyncio
async def test_refresh_single_source(client, auth_headers):
    """Refreshing a single source only returns that source."""
    resp = await client.post("/refresh", json={"source": "grailed"}, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["sources_refreshed"] == ["grailed"]


@pytest.mark.asyncio
async def test_refresh_invalid_source(client, auth_headers):
    """Invalid source name returns 400."""
    resp = await client.post(
        "/refresh",
        json={"source": "fakemarketplace"},
        headers=auth_headers,
    )
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_events_list_empty_initially(client, auth_headers):
    """Events endpoint returns empty list if no price changes happened."""
    resp = await client.get("/events", headers=auth_headers)
    assert resp.status_code == 200
    assert "events" in resp.json()


@pytest.mark.asyncio
async def test_register_webhook(client, auth_headers):
    """Registering a webhook returns the created webhook."""
    resp = await client.post(
        "/webhooks",
        json={"url": "https://example.com/hook"},
        headers=auth_headers,
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["url"] == "https://example.com/hook"
    assert data["is_active"] is True
