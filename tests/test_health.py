import pytest


@pytest.mark.asyncio
async def test_health(client):
    r = await client.get("/health")
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_login(client):
    
    r = await client.post("/users/create_account", 
                          json={
                              "id" : 24,
                              "name" : "ali4424"
                          })
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_create_user(client):
    r = await client.post("/users/create",
                          json = {
                              "name" : "al54424i9",
                              "age" : 23
                          })
    assert r.status_code == 201
    data = r.json()
    assert data["user_name"] == "al54424i9"


@pytest.mark.asyncio
async def test_auth(client):
    r = await client.post("/users/signin/auth", json={
        "username": "alia444424a@example.com",
        "password": "123456789",
        "role_name": "string",
        "name": "ali444424"
    })
    assert r.status_code == 200
    jwt = r.json()["access_token"]
    print (jwt)