import pytest


@pytest.mark.asyncio
async def test_register_success(client):
    """User can register with valid credentials."""
    resp = await client.post("/auth/register", json={
        "email": "new@example.com",
        "password": "password123",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "new@example.com"
    assert "api_key" in data
    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    """Duplicate email registration should return 400."""
    payload = {"email": "dup@example.com", "password": "pass123"}
    await client.post("/auth/register", json=payload)
    resp = await client.post("/auth/register", json=payload)
    assert resp.status_code == 400
    assert "already registered" in resp.json()["detail"]


@pytest.mark.asyncio
async def test_login_success(client):
    """Valid credentials return a JWT token."""
    await client.post("/auth/register", json={
        "email": "login@example.com",
        "password": "mypassword",
    })
    resp = await client.post("/auth/token", data={
        "username": "login@example.com",
        "password": "mypassword",
    })
    assert resp.status_code == 200
    assert "access_token" in resp.json()
    assert resp.json()["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    """Wrong password should return 401."""
    await client.post("/auth/register", json={
        "email": "wp@example.com",
        "password": "correctpass",
    })
    resp = await client.post("/auth/token", data={
        "username": "wp@example.com",
        "password": "wrongpass",
    })
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_protected_route_without_token(client):
    """Accessing protected endpoints without token returns 401."""
    resp = await client.get("/products")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_protected_route_with_invalid_token(client):
    """Malformed token should return 401."""
    resp = await client.get(
        "/products",
        headers={"Authorization": "Bearer notavalidtoken"},
    )
    assert resp.status_code == 401
