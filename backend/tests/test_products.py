import pytest


@pytest.mark.asyncio
async def test_list_products_empty(client, auth_headers):
    """Empty DB returns empty list, not an error."""
    resp = await client.get("/products", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert data["total"] == 0
    assert data["page"] == 1


@pytest.mark.asyncio
async def test_refresh_populates_products(client, auth_headers):
    """Triggering refresh inserts products from all 3 sources."""
    resp = await client.post("/refresh", json={}, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["products_new"] > 0
    assert len(data["sources_refreshed"]) == 3


@pytest.mark.asyncio
async def test_list_products_after_refresh(client, auth_headers):
    """After refresh, product list is populated."""
    await client.post("/refresh", json={}, headers=auth_headers)
    resp = await client.get("/products", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["total"] > 0


@pytest.mark.asyncio
async def test_filter_by_source(client, auth_headers):
    """Source filter returns only products from that marketplace."""
    await client.post("/refresh", json={}, headers=auth_headers)
    resp = await client.get("/products?source=grailed", headers=auth_headers)
    assert resp.status_code == 200
    for item in resp.json()["items"]:
        assert item["source"] == "grailed"


@pytest.mark.asyncio
async def test_filter_by_price_range(client, auth_headers):
    """Price range filter returns only products in range."""
    await client.post("/refresh", json={}, headers=auth_headers)
    resp = await client.get("/products?price_min=100&price_max=500", headers=auth_headers)
    assert resp.status_code == 200
    for item in resp.json()["items"]:
        assert 100 <= item["current_price"] <= 500


@pytest.mark.asyncio
async def test_get_product_detail(client, auth_headers):
    """Single product detail returns all required fields."""
    await client.post("/refresh", json={}, headers=auth_headers)
    list_resp = await client.get("/products?limit=1", headers=auth_headers)
    items = list_resp.json()["items"]
    assert len(items) > 0
    product_id = items[0]["id"]

    resp = await client.get(f"/products/{product_id}", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == product_id
    assert "external_id" in data
    assert "current_price" in data


@pytest.mark.asyncio
async def test_get_product_not_found(client, auth_headers):
    """Non-existent product ID returns 404."""
    resp = await client.get(
        "/products/00000000-0000-0000-0000-000000000000",
        headers=auth_headers,
    )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_price_history_populated(client, auth_headers):
    """After refresh, products have price history."""
    await client.post("/refresh", json={}, headers=auth_headers)
    list_resp = await client.get("/products?limit=1", headers=auth_headers)
    product_id = list_resp.json()["items"][0]["id"]

    resp = await client.get(f"/products/{product_id}/history", headers=auth_headers)
    assert resp.status_code == 200
    assert len(resp.json()["price_history"]) >= 1
