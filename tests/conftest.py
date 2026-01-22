import pytest, httpx
from httpx import AsyncClient
from asgi_lifespan import LifespanManager
import pytest_asyncio

from app.main import app


@pytest_asyncio.fixture
async def client():
    async with LifespanManager(app):
        transport = httpx.ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac


