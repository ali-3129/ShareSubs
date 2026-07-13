import pytest

from jose import jwt
from sqlalchemy import select
from app.infrastructure.bootstrap import ALGORITHM, SECRET_KEY
from app.data.Repository.user_db import UserModel


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

@pytest.mark.asyncio
async def test_me(client, login):
    user = jwt.decode(login, SECRET_KEY, ALGORITHM)
    assert user["sub"] == "aliaa44@example.com"
    print(user["sub"])
    print(login)

@pytest.mark.asyncio
async def test_fake_token(client, create_fake_token):
    response = await client.post("/users/signin/auth", json={
        "username": "alia444425a@example.com",
        "password": "123456789",
        "role_name": "string",
        "name": "ali444425"
    })

    token = response.json()["access_token"]
    current_user = await client.get("/users/me", 
                            headers={"Authorization": f"Bearer {token}"})
    assert current_user.status_code == 401


@pytest.mark.asyncio
async def test_appi_db_check(client):
    r = await client.patch("users/db/update/1", json={
        "name": "Ali"
    })
    res = r.json()["response"]
    assert res == "ok"


@pytest.mark.asyncio
async def test_db_check(fake_session):
    session = fake_session
    res = await session.execute(
        select(UserModel).where(UserModel.id == 1)
    )
    print(res)